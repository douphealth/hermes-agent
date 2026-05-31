# Repository Portfolio Inventory + External Platform Enrichment

Use when the user wants a SOTA/enterprise management table for many repos and connected app platforms (GitHub, Cloudflare Pages/DNS, Lovable, Supabase, etc.).

## Core workflow

1. **Start with live GitHub metadata**
   - Use authenticated GitHub if available; public API is enough for public repos.
   - Capture: name, full_name, html_url, clone_url, language, visibility/private, description, default_branch, created_at, updated_at, pushed_at, archived, disabled, fork, homepage, topics.
   - If the user asks to make repos public first, verify owner login, list `visibility=private&affiliation=owner`, PATCH `private:false`, then re-list to prove `0` private owned repos remain.

2. **Merge user-provided business mapping, but do not treat it as the only source**
   - Normalize by repo name and clone URL.
   - Preserve user labels separately from GitHub-verified fields: `Display / Product Name`, `Business Description`, `GitHub Verified Description`, `Data Source`, `Missing Data / Next Action`.
   - Do not overwrite live GitHub truth with stale provided visibility/language.

3. **Create an actual artifact, not a chat-only table**
   - Prefer `.xlsx` plus `.csv` plus optional markdown backup.
   - For Excel, include multiple sheets:
     - Portfolio Management
     - Executive Summary
     - Needs Enrichment
     - Platform-specific inventories (Cloudflare Pages, DNS, Lovable probe, Supabase, etc.)
   - Freeze header row, add filters/table style, widen URL/notes columns, use color fills for verified/missing/matched status.

4. **Exhaust public/API inference before asking the user to do manual work**
   - If a private dashboard is behind OAuth (Lovable/Google, etc.), first probe all known public project/app URLs, DNS TXT verification records, Cloudflare custom domains, GitHub repo bindings, and public app HTML.
   - Only after producing a useful enriched artifact should you say what remains impossible without session/API access.
   - Do not ask the user to manually export/screenshot everything as the first move; this is a high-friction failure mode for this user.

## Cloudflare enrichment pattern

Cloudflare may split Pages and DNS across accounts:
- A token/account can successfully list Pages projects but return `success:true` and `0` zones.
- That means the token is valid for its account, but the DNS zones likely live in a different Cloudflare account/email — not necessarily wrong permissions.

For Pages:
- `GET /accounts/{account_id}/pages/projects` may reject `per_page=50/100` with `Invalid list options`; use default `per_page=10` and page through with `?page=N`.
- Capture: project name, subdomain, custom domains, source config owner/repo_name, production_branch, build command, output dir, root dir, latest deployments.

For DNS:
- Use account/token that can see zones.
- Capture every zone and `GET /zones/{zone_id}/dns_records`.
- Map portfolio rows by exact hostname from Website URL / Cloudflare Page / custom domains, then by CNAME target to `*.pages.dev`.

## Lovable public enrichment pattern

When Lovable uses Google login:
- Emails alone are not credentials; private dashboard cannot be accessed without OAuth session.
- Still do public enrichment first:
  - Probe provided `https://lovable.dev/projects/<uuid>` URLs. Many return HTTP 200 with title `Login`, proving the project URL exists but internal details require auth.
  - Probe public `.lovable.app` URLs and custom domains for HTTP status, title, meta description, visible GitHub links, and Supabase URLs.
  - Search Cloudflare DNS for `_lovable` TXT verification records.
- Add explicit columns: Project URL Status, Page Title, Public Access Result, Published App Status, Published App Title, Public GitHub Links, Public Supabase URLs, Verification DNS Clues, Confidence, Notes.

## Supabase enrichment pattern

Without a Supabase PAT/project export, preserve user-provided Supabase account/project URL/publishable key and flag rows needing verification.
With a PAT, enrich from project list: org, project ref, name, region, status, API URL, anon/publishable key if exposed, created date, linked functions/storage/domains if available.

## Recommended columns

Minimum enterprise portfolio columns:
- #, Status, Category, Display/Product Name, Repository Name, Language, Visibility
- GitHub Verified Description, Business Description, GitHub Link, Git Clone URL
- Default Branch, Created At, Updated At, Pushed At, Archived, Fork, Topics, Homepage Field
- Cloudflare Page, CF Project Name, CF Pages URL, CF Custom Domains, CF Repo Binding, CF Production Branch, CF Latest Deployment, CF Match Quality
- DNS Zone, DNS Record Type, DNS Record Name, DNS Record Target, DNS Proxied, DNS TTL, DNS Match Quality
- Lovable App, Lovable Project URL Status, Lovable Public Access Result, Lovable Published App Status, Lovable Confidence
- Website URL, Supabase Account, Supabase Project URL, Supabase Publishable Key
- Data Source, Management Notes, Missing Data / Next Action

## User-facing reporting

Keep the report terse and artifact-first:
- Attach the workbook/CSV.
- State counts verified: repo rows, public/private counts, Pages projects, DNS zones/records, exact matches, unmatched rows.
- Clearly separate: `verified live`, `user-provided`, `publicly inferred`, `requires private session/API`.
- If the user is frustrated, do not defend the limitation; immediately do the next public/API inference step and update the artifact.
