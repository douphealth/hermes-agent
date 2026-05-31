#!/usr/bin/env python3
"""Mirror the active Hermes runtime skill library into a portable repo snapshot.

This is intentionally conservative: it copies ~/.hermes/skills into
hermes-skills-current/ while excluding runtime/cache noise and redacting only
high-confidence secrets. The snapshot is for disaster recovery: clone the repo,
copy active/* back to ~/.hermes/skills, and the agent gets its local skill brain
back without copying credentials.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
from datetime import datetime, timezone
from pathlib import Path

DEFAULT_SOURCE = Path(os.environ.get("HERMES_SKILLS_SOURCE", Path.home() / ".hermes" / "skills"))
DEFAULT_DEST = Path(__file__).resolve().parents[1] / "hermes-skills-current"

EXCLUDE_DIRS = {
    ".git",
    "__pycache__",
    ".mypy_cache",
    ".pytest_cache",
    ".ruff_cache",
    "node_modules",
    "venv",
    ".venv",
    "dist",
    "build",
    "logs",
    "locks",
    "tmp",
    "temp",
}
EXCLUDE_FILES = {
    ".usage.json",
    ".usage.json.lock",
    ".curator_state",
    ".bundled_manifest",
    ".DS_Store",
}
TEXT_SUFFIXES = {
    ".md",
    ".txt",
    ".json",
    ".yaml",
    ".yml",
    ".toml",
    ".py",
    ".sh",
    ".bash",
    ".js",
    ".ts",
    ".css",
    ".html",
    ".xml",
    ".csv",
}

SECRET_PATTERNS: list[tuple[re.Pattern[str], str]] = [
    (re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----.*?-----END [A-Z ]*PRIVATE KEY-----", re.S), "[REDACTED_PRIVATE_KEY]"),
    (re.compile(r"\bghp_[A-Za-z0-9_]{30,}\b"), "[REDACTED_GITHUB_TOKEN]"),
    (re.compile(r"\bgithub_pat_[A-Za-z0-9_]{40,}\b"), "[REDACTED_GITHUB_TOKEN]"),
    (re.compile(r"\bsk-(?:proj-)?[A-Za-z0-9_-]{32,}\b"), "[REDACTED_OPENAI_KEY]"),
    (re.compile(r"\bsk-ant-[A-Za-z0-9_-]{32,}\b"), "[REDACTED_ANTHROPIC_KEY]"),
    (re.compile(r"\b[A-Za-z0-9_-]{20,}\.[A-Za-z0-9_-]{20,}\.[A-Za-z0-9_-]{20,}\b"), "[REDACTED_JWT]"),
    (
        re.compile(
            r"(?i)(api[_-]?key|secret|token|password|passwd|pwd|authorization)\s*[:=]\s*['\"]?([^'\"\s]{3,})['\"]?"
        ),
        r"\1=[REDACTED]",
    ),
]


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8", errors="ignore")).hexdigest()[:16]


def is_text_file(path: Path) -> bool:
    if path.suffix.lower() in TEXT_SUFFIXES:
        return True
    try:
        chunk = path.read_bytes()[:4096]
    except OSError:
        return False
    return b"\0" not in chunk


def scrub_text(text: str) -> tuple[str, int]:
    total = 0
    for pattern, repl in SECRET_PATTERNS:
        text, n = pattern.subn(repl, text)
        total += n
    return text, total


def include_file(path: Path) -> bool:
    parts = set(path.parts)
    if parts & EXCLUDE_DIRS:
        return False
    if path.name in EXCLUDE_FILES:
        return False
    if path.suffix in {".pyc", ".pyo", ".log", ".lock"}:
        return False
    return True


def read_description(skill_md: Path) -> str:
    try:
        text = skill_md.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return ""
    match = re.search(r"(?m)^description:\s*['\"]?(.*?)['\"]?\s*$", text)
    if match:
        return match.group(1).strip()
    for line in text.splitlines():
        if line.strip() and not line.startswith("---") and not line.startswith("#"):
            return line.strip()[:200]
    return ""


def copy_tree(source: Path, dest: Path) -> dict:
    if dest.exists():
        shutil.rmtree(dest)
    dest.mkdir(parents=True, exist_ok=True)

    files = 0
    redactions = 0
    skill_entries: list[dict] = []

    for skill_md in sorted(source.rglob("SKILL.md")):
        rel_skill_dir = skill_md.parent.relative_to(source)
        status = "archive" if rel_skill_dir.parts and rel_skill_dir.parts[0] == ".archive" else "active"
        if status == "archive":
            out_skill_dir = dest / "archive" / Path(*rel_skill_dir.parts[1:])
            category = ".archive"
        else:
            out_skill_dir = dest / "active" / rel_skill_dir
            category = rel_skill_dir.parts[0] if rel_skill_dir.parts else "uncategorized"

        content_hash = ""
        for path in sorted(skill_md.parent.rglob("*")):
            rel_file = path.relative_to(skill_md.parent)
            if path.is_dir() or not include_file(rel_file):
                continue
            out_file = out_skill_dir / rel_file
            out_file.parent.mkdir(parents=True, exist_ok=True)
            if is_text_file(path):
                text = path.read_text(encoding="utf-8", errors="ignore")
                scrubbed, count = scrub_text(text)
                redactions += count
                out_file.write_text(scrubbed, encoding="utf-8")
                if rel_file.as_posix() == "SKILL.md":
                    content_hash = sha256_text(scrubbed)
            else:
                shutil.copy2(path, out_file)
            shutil.copystat(path, out_file, follow_symlinks=False)
            files += 1

        skill_entries.append(
            {
                "name": skill_md.parent.name,
                "status": status,
                "category": category,
                "source_path": str(rel_skill_dir),
                "snapshot_path": str(out_skill_dir.relative_to(dest)),
                "description": read_description(skill_md),
                "hash": content_hash,
            }
        )

    return {"files": files, "redactions": redactions, "skills": skill_entries}


def write_readme(dest: Path, manifest: dict) -> None:
    active = [s for s in manifest["skills"] if s["status"] == "active"]
    archived = [s for s in manifest["skills"] if s["status"] == "archive"]
    lines = [
        "# Hermes Skills Current Snapshot",
        "",
        "Portable disaster-recovery snapshot of the local Hermes runtime skill library.",
        "",
        "## Restore on a fresh PC",
        "",
        "```bash",
        "git clone https://github.com/douphealth/hermes-agent ~/.hermes/hermes-agent",
        "mkdir -p ~/.hermes/skills",
        "rsync -a ~/.hermes/hermes-agent/hermes-skills-current/active/ ~/.hermes/skills/",
        "# Optional archived skills:",
        "# rsync -a ~/.hermes/hermes-agent/hermes-skills-current/archive/ ~/.hermes/skills/.archive/",
        "hermes skills list",
        "```",
        "",
        "## Snapshot metadata",
        "",
        f"- Generated at: `{manifest['generated_at']}`",
        f"- Active skills: `{manifest['active_skill_count']}`",
        f"- Archived skills: `{manifest['archived_skill_count']}`",
        f"- Files copied: `{manifest['file_count']}`",
        f"- Secret redactions: `{manifest['redaction_count']}`",
        "",
        "## Active skills",
        "",
    ]
    for skill in active:
        lines.append(f"- `{skill['snapshot_path']}` — {skill.get('description','')}")
    lines += ["", "## Archived skills", ""]
    for skill in archived:
        lines.append(f"- `{skill['snapshot_path']}` — {skill.get('description','')}")
    dest.joinpath("README.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, default=DEFAULT_SOURCE)
    parser.add_argument("--dest", type=Path, default=DEFAULT_DEST)
    args = parser.parse_args()

    source = args.source.expanduser().resolve()
    dest = args.dest.expanduser().resolve()
    if not source.exists():
        raise SystemExit(f"skills source not found: {source}")

    result = copy_tree(source, dest)
    active_count = sum(1 for s in result["skills"] if s["status"] == "active")
    archived_count = sum(1 for s in result["skills"] if s["status"] == "archive")
    manifest = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "source": str(source),
        "active_skill_count": active_count,
        "archived_skill_count": archived_count,
        "active_count": active_count,
        "archived_count": archived_count,
        "file_count": result["files"],
        "redaction_count": result["redactions"],
        "skills": result["skills"],
    }
    dest.joinpath("MANIFEST.json").write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    write_readme(dest, manifest)
    print(json.dumps({k: manifest[k] for k in ["active_skill_count", "archived_skill_count", "file_count", "redaction_count"]}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
