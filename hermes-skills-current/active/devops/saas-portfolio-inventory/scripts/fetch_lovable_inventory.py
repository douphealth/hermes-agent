#!/usr/bin/env python3
"""
Fetch Lovable workspace/project inventory from a Cookie-Editor JSON export.

Usage:
  python fetch_lovable_inventory.py /path/to/lovable.dev_cookies.json /tmp/lovable_inventory.json

Security:
  - Does not print cookie/session values.
  - Writes raw Lovable API output to the requested output path; treat it as sensitive.
"""
import json
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

BASE = "https://api.lovable.dev"


def load_token(cookie_file: Path) -> str:
    cookies = json.loads(cookie_file.read_text())
    for c in cookies:
        if c.get("name") == "lovable-session-id-v2" and c.get("value"):
            return c["value"]
    raise SystemExit("No lovable-session-id-v2 cookie found in export")


def make_get(headers):
    def get(endpoint: str):
        req = urllib.request.Request(BASE + endpoint, headers=headers)
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                txt = r.read().decode("utf-8", "ignore")
                return {"ok": True, "status": r.status, "data": json.loads(txt) if txt else None}
        except urllib.error.HTTPError as e:
            return {"ok": False, "status": e.code, "error": e.read(1000).decode("utf-8", "ignore")}
        except Exception as e:
            return {"ok": False, "status": None, "error": type(e).__name__ + ": " + str(e)}
    return get


def main():
    if len(sys.argv) != 3:
        raise SystemExit("Usage: fetch_lovable_inventory.py cookies.json output.json")
    cookie_file = Path(sys.argv[1])
    output_file = Path(sys.argv[2])
    token=[REDACTED]
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept": "application/json",
        "Origin": "https://lovable.dev",
        "Referer": "https://lovable.dev/",
        "Authorization": "Bearer " + token,
    }
    get = make_get(headers)

    out = {
        "source_cookie_file": str(cookie_file),
        "user_workspaces": get("/user/workspaces"),
        "pending_invitations": get("/user/workspace-invitations"),
        "workspaces": [],
    }
    workspaces = (out["user_workspaces"].get("data") or {}).get("workspaces") or []
    for w in workspaces:
        wid = w["id"]
        item = {"workspace": w}
        item["detail"] = get(f"/workspaces/{wid}")
        item["projects"] = get(f"/workspaces/{wid}/projects?limit=250")
        item["draft_projects"] = get(f"/workspaces/{wid}/projects/draft?limit=250")
        item["supabase_organizations"] = get(f"/workspaces/{wid}/supabase-organizations")
        projects = (item["projects"].get("data") or {}).get("projects") or []
        item["project_details"] = {}
        for p in projects:
            pid = p["id"]
            pd = {}
            endpoints = {
                "details": f"/projects/{pid}/details",
                "domains": f"/projects/{pid}/domains",
                "integrations": f"/projects/{pid}/integrations",
                "repo_accessibility": f"/projects/{pid}/repo-accessibility",
                "workspace": f"/projects/{pid}/workspace",
                "published_access": f"/workspaces/{wid}/projects/{pid}/published-access",
            }
            for name, endpoint in endpoints.items():
                pd[name] = get(endpoint)
                time.sleep(0.05)
            item["project_details"][pid] = pd
        out["workspaces"].append(item)

    output_file.write_text(json.dumps(out, indent=2), encoding="utf-8")
    project_count = sum(len(((w.get("projects", {}).get("data") or {}).get("projects") or [])) for w in out["workspaces"])
    supabase_count = sum(len((w.get("supabase_organizations", {}).get("data") or [])) for w in out["workspaces"])
    pending = len(((out.get("pending_invitations", {}).get("data") or {}).get("invitations") or []))
    print(f"workspaces {len(workspaces)}")
    print(f"projects {project_count}")
    print(f"supabase_org_connections {supabase_count}")
    print(f"pending_invites {pending}")
    print(str(output_file))


if __name__ == "__main__":
    main()
