# Bulk Repo Visibility + Enterprise Portfolio Inventory

Use this reference when a user asks to bulk-change repository visibility or create a full management table across GitHub repos plus app/deployment providers.

## Bulk make all owner repos public

Workflow:
1. Verify auth method. If `gh` is unavailable, use GitHub REST with a token from env/runtime only.
2. Verify the authenticated login matches the target owner with `GET /user` before changing anything.
3. List candidate repos with `GET /user/repos?visibility=private&affiliation=owner&per_page=100&page=N`.
4. Filter strictly: `repo.private == true` and `repo.owner.login.lower() == target.lower()`.
5. Patch each repo: `PATCH /repos/{owner}/{repo}` body `{"private": false}`.
6. Verify by re-listing private owner-affiliated repos and reporting `REMAINING_PRIVATE_OWNED_COUNT`.
7. Tell the user to revoke a one-off PAT after the operation.

Avoid:
- Do not rely on public `/users/{owner}/repos` for private repo discovery.
- Do not store PATs in memory or skills.
- Do not claim all repos are public until the private-owner re-list returns zero.

## Enterprise portfolio table shape

For “SOTA management table” requests, produce files, not a chat table. Deliver `.xlsx` and `.csv`.

Recommended workbook sheets:
- `Portfolio Management`: one row per GitHub repo/project, enriched with app/deployment/database data.
- `Executive Summary`: generated timestamp, owner, row counts, public/private counts, enrichment counts, accuracy notes.
- `Needs Enrichment`: missing Cloudflare/Lovable/Supabase/domain fields and the credential/API needed.
- Provider-specific inventory sheets when credentials are available, e.g. `Cloudflare Pages Inventory`.

Recommended columns:
- Status, Category, Display/Product Name, Repository Name, Language, Visibility
- GitHub verified description, business description, GitHub link, clone URL, default branch
- Created/updated/pushed timestamps, archived, fork, topics
- Cloudflare Page, Lovable App, Website URL
- Supabase account, project URL/ref, publishable/anon key
- Provider match fields: repo binding, project name, custom domains, latest deployment, match quality
- Data Source, Management Notes, Missing Data / Next Action

Accuracy pattern:
- Fetch GitHub metadata live first.
- Merge user-provided business data by normalized repo name.
- Keep GitHub-verified fields separate from user-provided fields.
- Add `Data Source` and `Match Quality` columns so future users can audit provenance.
- Verify row counts, key example rows, visibility counts, and workbook structure before final response.

## Cloudflare Pages enrichment

Required Cloudflare token permissions:
- Account → Cloudflare Pages → Read
- Account → Account Settings → Read
- Zone → Zone → Read
- Zone → DNS → Read

Pages endpoints:
- `GET /accounts` to find account IDs.
- `GET /accounts/{account_id}/pages/projects?page=N` for projects.
- `GET /accounts/{account_id}/pages/projects/{project_name}/deployments?page=N` for deployments.
- `GET /accounts/{account_id}/pages/projects/{project_name}/domains` for custom domains; some accounts may expose `custom_domains` variants, so retry alternatives if needed.

Observed Cloudflare quirk:
- Pages project listing accepted `page=N` with default page size but rejected `per_page=50` or `per_page=100` with `Invalid list options provided. Review the page or per_page parameter.` Do not assume large `per_page` is valid for Pages; paginate with default page size if needed.

Useful Cloudflare fields:
- Project name
- Pages subdomain (`{project}.pages.dev`)
- Custom domains
- Source config: GitHub owner/repo binding, production branch, build command, output directory, root directory
- Latest deployment time, URL, environment/stage

Cloudflare zones/DNS:
- If `/zones` returns zero while Pages works, the token can read Pages but lacks/was not scoped to zones. Ask for a token/resource scope that includes the relevant zones with `Zone:Zone Read` and `Zone:DNS Read`.

## Lovable and Supabase enrichment needs

Lovable:
- Best: project export/list containing project name, Lovable project URL, GitHub repo URL, published app URL, custom domain, Supabase integration.
- Alternative: browser/session/account access if no export/API is available.

Supabase:
- Need a Supabase Personal Access Token from dashboard account tokens.
- Extract org, project name/ref, API URL, status/region/created date, anon/publishable key if available.
- Do not request service-role keys unless backend/admin inspection is explicitly needed.
