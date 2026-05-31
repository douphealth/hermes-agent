#!/usr/bin/env python3
"""Enterprise GEO/AEO runner for Hermes Authority Engine.

Runs GEO Optimizer and Searchstack via uvx, saving evidence artifacts for SEO/GEO/AEO audits.
This script intentionally does not publish changes. It creates staging outputs only.
"""
from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse


def run(cmd: list[str], out_file: Path, timeout: int = 300, cwd: Path | None = None) -> dict:
    started = datetime.now(timezone.utc).isoformat()
    try:
        p = subprocess.run(cmd, text=True, capture_output=True, timeout=timeout, cwd=str(cwd) if cwd else None)
        output = (p.stdout or "") + (("\nSTDERR:\n" + p.stderr) if p.stderr else "")
        out_file.write_text(output, encoding="utf-8")
        return {"cmd": cmd, "exit_code": p.returncode, "output_file": str(out_file), "started": started, "bytes": len(output), "cwd": str(cwd) if cwd else None}
    except subprocess.TimeoutExpired as e:
        output = (e.stdout or "") + (e.stderr or "")
        out_file.write_text(output, encoding="utf-8")
        return {"cmd": cmd, "exit_code": 124, "output_file": str(out_file), "started": started, "timeout": timeout, "bytes": len(output)}
    except FileNotFoundError as e:
        out_file.write_text(str(e), encoding="utf-8")
        return {"cmd": cmd, "exit_code": 127, "output_file": str(out_file), "started": started, "error": str(e)}


def safe_name(url: str) -> str:
    host = urlparse(url).netloc or re.sub(r"\W+", "-", url)
    return re.sub(r"[^a-zA-Z0-9_.-]+", "-", host).strip("-") or "site"


def try_json(path: Path):
    try:
        text = path.read_text(encoding="utf-8")
        # Some CLIs may write warnings before JSON. Try exact first, then object slice.
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            start, end = text.find("{"), text.rfind("}")
            if start >= 0 and end > start:
                return json.loads(text[start : end + 1])
    except Exception:
        return None
    return None


def summarize_geo(data) -> dict:
    if not isinstance(data, dict):
        return {"parseable": False}
    summary = {"parseable": True}
    for key in ("score", "grade", "url", "domain"):
        if key in data:
            summary[key] = data[key]
    # tolerate different output schemas
    findings = []
    for key in ("issues", "recommendations", "checks", "results"):
        val = data.get(key)
        if isinstance(val, list):
            findings.extend(val[:20])
        elif isinstance(val, dict):
            findings.extend(list(val.items())[:20])
    summary["sample_findings"] = findings[:12]
    return summary


def write_searchstack_config(out_dir: Path, url: str, sitemap: str | None) -> Path:
    domain = urlparse(url).netloc or url.replace("https://", "").replace("http://", "").strip("/")
    cfg = out_dir / ".searchstack.toml"
    cfg.write_text(
        f'''domain = "{domain}"
sitemap = "{sitemap or url.rstrip('/') + '/sitemap.xml'}"

# Optional integrations. Fill only when credentials are available; never commit secrets.
# [openai]
# api_key=[REDACTED]
# [perplexity]
# api_key=[REDACTED]
# [anthropic]
# api_key=[REDACTED]
# [gsc]
# service_account = "/absolute/path/to/service-account.json"
# property = "https://{domain}/"
''',
        encoding="utf-8",
    )
    return cfg


def main() -> int:
    ap = argparse.ArgumentParser(description="Run enterprise GEO/AEO/AI-visibility audit evidence collection.")
    ap.add_argument("--url", required=True, help="Canonical site or page URL, e.g. https://example.com")
    ap.add_argument("--sitemap", help="Sitemap URL. If omitted, tools auto-detect where possible.")
    ap.add_argument("--max-urls", type=int, default=50, help="Max sitemap URLs for GEO batch audit.")
    ap.add_argument("--out", default=None, help="Output directory. Default: ./geo-aeo-<host>-<timestamp>")
    ap.add_argument("--skip-searchstack", action="store_true", help="Skip searchstack technical checks.")
    ap.add_argument("--skip-html", action="store_true", help="Skip GEO HTML report generation.")
    args = ap.parse_args()

    if not shutil.which("uvx"):
        print("ERROR: uvx not found. Install uv or use permanent tool installs.", file=sys.stderr)
        return 127

    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    out_dir = Path(args.out or f"geo-aeo-{safe_name(args.url)}-{stamp}").resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    manifest: list[dict] = []

    # GEO Optimizer single URL JSON
    geo_home_json = out_dir / "geo-audit-url.json"
    manifest.append(run([
        "uvx", "--from", "geo-optimizer-skill", "geo", "audit",
        "--url", args.url, "--format", "json", "--output", str(geo_home_json),
    ], out_dir / "geo-audit-url.command.log", timeout=300))
    # When --output is used, stdout log may be tiny; include actual target status.
    manifest[-1]["artifact"] = str(geo_home_json)

    if not args.skip_html:
        geo_html = out_dir / "geo-audit-url.html"
        manifest.append(run([
            "uvx", "--from", "geo-optimizer-skill", "geo", "audit",
            "--url", args.url, "--format", "html", "--output", str(geo_html),
        ], out_dir / "geo-audit-url-html.command.log", timeout=300))
        manifest[-1]["artifact"] = str(geo_html)

    if args.sitemap:
        geo_sitemap_json = out_dir / "geo-audit-sitemap.json"
        manifest.append(run([
            "uvx", "--from", "geo-optimizer-skill", "geo", "audit",
            "--sitemap", args.sitemap, "--max-urls", str(args.max_urls), "--concurrency", "5",
            "--format", "json", "--output", str(geo_sitemap_json),
        ], out_dir / "geo-audit-sitemap.command.log", timeout=max(300, args.max_urls * 20)))
        manifest[-1]["artifact"] = str(geo_sitemap_json)

        llms_file = out_dir / "llms.txt"
        manifest.append(run([
            "uvx", "--from", "geo-optimizer-skill", "geo", "llms",
            "--base-url", args.url, "--sitemap", args.sitemap, "--output", str(llms_file),
        ], out_dir / "geo-llms.command.log", timeout=300))
        manifest[-1]["artifact"] = str(llms_file)

    if not args.skip_searchstack:
        cfg = write_searchstack_config(out_dir, args.url, args.sitemap)
        for name, cmd in [
            ("searchstack-llms-check.log", ["uvx", "--from", "searchstack", "searchstack", "llms", "check"]),
            ("searchstack-meta.log", ["uvx", "--from", "searchstack", "searchstack", "meta"]),
            ("searchstack-schema.log", ["uvx", "--from", "searchstack", "searchstack", "schema"]),
            ("searchstack-links.log", ["uvx", "--from", "searchstack", "searchstack", "links"]),
            ("searchstack-onpage-home.log", ["uvx", "--from", "searchstack", "searchstack", "onpage", args.url]),
        ]:
            manifest.append(run(cmd, out_dir / name, timeout=300, cwd=out_dir))
            manifest[-1]["cwd_config"] = str(cfg)

    geo_summary = summarize_geo(try_json(geo_home_json))
    summary = {
        "url": args.url,
        "sitemap": args.sitemap,
        "created_at": stamp,
        "out_dir": str(out_dir),
        "geo_home_summary": geo_summary,
        "commands": manifest,
        "next_steps": [
            "Read geo-audit-url.json/html for score and prioritized gaps.",
            "Review generated llms.txt as a staging draft; do not publish until low-value/noindex/redirect URLs are removed.",
            "Use searchstack logs for technical checks and configure APIs before AI citation monitoring.",
            "Convert findings into KEEP/REFRESH/MERGE/301/410/NOINDEX map before requesting indexing.",
        ],
    }
    (out_dir / "manifest.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    (out_dir / "README.md").write_text(
        "# Enterprise GEO/AEO Audit Evidence\n\n"
        f"URL: {args.url}\n\nSitemap: {args.sitemap or 'not provided'}\n\n"
        f"GEO summary: `{json.dumps(geo_summary)[:2000]}`\n\n"
        "Artifacts:\n" + "".join(f"- `{Path(x.get('artifact') or x.get('output_file')).name}` exit={x.get('exit_code')}\n" for x in manifest),
        encoding="utf-8",
    )
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
