---
name: saas-portfolio-inventory
description: Build authenticated enterprise portfolio inventories across GitHub, Cloudflare, Lovable, Supabase, and similar SaaS dashboards; merge data into management workbooks without storing secrets.
tags:
  - saas
  - inventory
  - lovable
  - cloudflare
  - supabase
  - github
  - portfolio
---

# SaaS Portfolio Inventory

Use this skill when the user wants a SOTA/enterprise-grade table, workbook, operating system, or inventory that cross-links repositories, deployments, DNS, domains, low-code app builders, and backend providers. Typical stack: GitHub org/repos, Cloudflare Pages/DNS, Lovable workspaces/projects, Supabase orgs/projects, custom domains, and project management sheets.

## Operating posture for this user/class of task

- **Execute first, minimize manual chores.** Public/API/browser inference comes before asking the user to export screenshots or hand-fill tables.
- **Ask for one exact access item at a time** when blocked. Do not list a confusing menu after the user has already chosen a path.
- **Never persist secrets.** API tokens, cookies, session IDs, Supabase keys, passwords, and invite links are runtime inputs only. Redact sensitive values in outputs and never place them in memory/skills/workbooks unless the user explicitly asked for a secrets vault (normally: do not).
- **Create artifacts, not explanations.** Deliver the workbook/CSV/report files and concrete counts.
- **Enterprise workbook standard:** multi-sheet XLSX, filters/tables, frozen headers, clear risk/action fields, relationship matrix, unmatched/orphan sheets, and traceable match method/confidence columns.

## Access workflow priority

1. **Public probes first:** GitHub public API, DNS, published URLs, Cloudflare public hostnames, Lovable `.lovable.app` URLs.
2. **Read-only API tokens:** GitHub/Cloudflare/Supabase PATs with least privilege where possible.
3. **Workspace invite/collaborator:** For Lovable or similar dashboards, prefer temporary workspace member/editor access over primary account credentials.
4. **Session cookie export:** If OAuth blocks bot login, ask the user to log in locally and export only the target domain cookies. Use the cookie to call APIs or load browser session.
5. **Screenshots/video last:** Only if no authenticated API/session path works.

## Lovable authenticated inventory pattern

When the user provides Lovable workspace invite links:

1. Open one invite. If redirected to `/login?redirect=/workspace-invite/...`, explain the precise blocker: the invite must be accepted by a logged-in Lovable user.
2. Best path:
   - User creates/uses a temporary Lovable/Google account.
   - User accepts all workspace invite links while logged in.
   - User exports cookies only for `lovable.dev` / `.lovable.dev` using Cookie-Editor JSON.
3. Load the cookie JSON from the uploaded document. Do **not** print cookie values.
4. Extract `lovable-session-id-v2` and call Lovable's API with:
   - `Authorization=[REDACTED] <lovable-session-id-v2>`
   - `Origin: https://lovable.dev`
   - `Referer: https://lovable.dev/`
   - normal browser `User-Agent`
5. Useful endpoints observed:
   - `GET https://api.lovable.dev/user/workspaces`
   - `GET https://api.lovable.dev/user/workspace-invitations`
   - `GET https://api.lovable.dev/workspaces/{workspace_id}`
   - `GET https://api.lovable.dev/workspaces/{workspace_id}/projects?limit=250`
   - `GET https://api.lovable.dev/workspaces/{workspace_id}/supabase-organizations`
   - `GET https://api.lovable.dev/projects/{project_id}/details`
   - `GET https://api.lovable.dev/projects/{project_id}/domains`
   - `GET https://api.lovable.dev/projects/{project_id}/integrations`
   - `GET https://api.lovable.dev/projects/{project_id}/repo-accessibility`
   - `GET https://api.lovable.dev/projects/{project_id}/workspace`
   - `GET https://api.lovable.dev/workspaces/{workspace_id}/projects/{project_id}/published-access`
6. Expected high-value fields:
   - workspace id/name/owner/plan/member role
   - project id/name/display name
   - published `.lovable.app` URL
   - custom domains + status
   - GitHub owner/repo/repo id/is_github/accessibility
   - status/is_published/publish_visibility/published_at
   - deployment target/status/branch/commit
   - latest commit/main branch/last edited/updated/created
   - Supabase org id/project id/managed-by-Lovable flag
   - integrations/memory item counts/AI gateway usage
   - generated description/initial prompt/screenshot URL

See `references/lovable-authenticated-api.md` for a condensed reference and redaction rules. See `references/lovable-cookie-dedupe.md` for checking whether multiple cookie exports are actually the same logged-in Lovable session. See `references/lovable-multi-invite-session-handling.md` for the proven invite-link + temporary-account + Cookie-Editor workflow, including how to respond when the user is confused by cookie/session terminology. See `references/lovable-cookie-inventory-and-health.md` for the account-by-account Cookie-Editor intake pattern, safe identity proof, redacted artifacts, and published URL health checks. See `references/lovable-project-chat-and-upgrade.md` for using authenticated Lovable project chat APIs to submit upgrade prompts, and for the exact CAPTCHA-blocker fallback. Use `scripts/fetch_lovable_inventory.py` as a reusable authenticated Lovable API fetcher when a Cookie-Editor JSON export is available.

## Multiple authenticated cookie/session exports

When the user uploads multiple cookie exports labeled as different accounts, **verify the actual authenticated identity before merging**. Cookie files may be exported from the same browser session even when the user intended a different Lovable account.

If the user becomes frustrated or says they do not understand the access request, do not repeat abstract terms like “session” or “cookie” without context. Switch to one exact action in plain language: “Log into Lovable as the temporary account, open projects, click Cookie-Editor, Export JSON, upload that file.” For this user, access-blocker replies should be short, concrete, and single-next-step.

- Parse the JWT-like `lovable-session-id-v2` payload locally without printing the token. Compare safe claims such as `email`, `sub`/`user_id`, `name`, `iat`, and a short SHA-256 prefix of the token.
- Fetch `/user/workspaces` and compare workspace IDs/project IDs against the previous pull.
- If the authenticated identity and project/workspace sets are identical, do **not** regenerate or inflate the workbook. Report: same logged-in Lovable user, same workspace count, same project count, no new data.
- If the export is truly a different account/session, merge as another source and preserve source-session provenance columns.
- In user-facing replies, avoid abstract cookie/session explanations when the user is frustrated. State the concrete blocker and one exact next item, e.g. “This cookie is still logged in as `testing...`; export again after switching Google/Lovable accounts.”

## Matching strategy

For every inventory row, store both the matched object fields and a `Match Method` / `Match Confidence` column.

Recommended match order:

1. Exact SaaS project ID from dashboard URL.
2. Exact GitHub repo name/ID.
3. Exact published app slug/domain.
4. Exact custom domain / DNS hostname.
5. Normalized product/project display name.
6. Fuzzy/manual review only if marked as low confidence.

Always create unmatched/orphan sheets:

- Repos without deployment/app/backend.
- Cloudflare Pages without GitHub repo match.
- DNS domains without app/deployment match.
- Lovable projects without portfolio/repo match.
- Supabase projects without Lovable/GitHub/product match.

## Workbook schema guidance

Minimum sheets for enterprise management workbooks:

- `Control Center`: source counts, generated timestamp, coverage stats, blockers.
- `Master Portfolio OS`: one row per product/repo/site with enriched cross-links.
- `Action Queue`: prioritized fixes with owner/source/evidence.
- `Relationship Matrix`: repo ↔ app ↔ domain ↔ deployment ↔ backend.
- `Domain & URL Map`: DNS, production URLs, Pages URLs, custom domains.
- `Supabase Matrix`: Supabase org/project/region/status/database host, redacted keys.
- Provider-specific verified inventories: e.g. `Lovable Verified Inventory`.
- Provider-specific unmatched sheets.

Use `openpyxl` for formatting: frozen headers, Excel tables, filters, widths, header fills, wrapping, and separate raw/verified sheets.

## Verification checklist

Before final response:

- For partial intake before the final XLSX, verify the uploaded Lovable cookie identity safely, fetch workspace/project counts, save redacted JSON/CSV artifacts, and run a published URL health probe so broken live apps are surfaced immediately.
- Re-open the XLSX with `openpyxl` to confirm sheets, row counts, and required columns exist.
- Confirm CSV/export paths exist and have nonzero size.
- Report concrete counts: repos, domains/DNS records, SaaS projects, workspaces, matches, unmatched.
- Include artifacts using `MEDIA:/absolute/path`.
- State remaining blind spots precisely, e.g. “Supabase direct PAT still needed for direct Supabase API verification,” not vague “more access needed.”

## Pitfalls

- Do not ask for primary Gmail/Lovable credentials if an invite-link + temporary-account + cookie-export route exists.
- Do not ask the user to understand cookies abstractly. Give exact steps: install Cookie-Editor, log into Lovable, accept links, export JSON for `lovable.dev`, upload/paste it.
- Do not preserve sensitive token/cookie/key values in scripts committed to skills or outputs. Runtime scripts should read local uploaded files and avoid logging values.
- Viewer roles may hide integrations/domains; for Lovable inventory, ask for Editor if Viewer is insufficient, while promising read-only behavior.
- Published Supabase anon/publishable keys may appear in API data. Treat them as sensitive-ish: include only if explicitly needed; otherwise redact or keep in private runtime artifacts.