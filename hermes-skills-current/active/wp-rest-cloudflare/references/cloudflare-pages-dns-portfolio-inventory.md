# Cloudflare Pages + DNS portfolio inventory pattern

Use this when building a source-of-truth workbook for many GitHub/Lovable/Cloudflare/Supabase projects.

## Token validation and account split pitfall

A correct Cloudflare token can still return zero zones if it was created under an account that owns Pages projects but not DNS zones. Do not tell the user the permissions are wrong until you verify:

```text
GET /user/tokens/verify
GET /accounts
GET /zones
GET /zones?name=example.com
GET /accounts/{account_id}/pages/projects
```

If Pages works but `/zones` returns success with `total_count: 0`, phrase it as:
- Token is valid.
- Pages account is visible.
- This specific account has no DNS zones visible to the API.
- DNS likely lives in a different Cloudflare account/email.

This avoids wrongly blaming the user when the token has the requested permissions.

## Pages API pagination quirk

Cloudflare Pages projects endpoint may reject high `per_page` values with:

```text
8000024 Invalid list options provided. Review the `page` or `per_page` parameter.
```

For Pages projects and deployments, use default pagination plus `page=N` instead of forcing `per_page=50/100`:

```text
GET /accounts/{account_id}/pages/projects?page=1
GET /accounts/{account_id}/pages/projects/{project_name}/deployments?page=1
```

For standard zones/DNS endpoints, `per_page=100&page=N` works.

## Fields to extract

From Pages projects:
- account name/id
- project name
- `subdomain` (`https://<project>.pages.dev`)
- source owner/repo binding
- production branch
- build command
- destination/output directory
- root directory
- custom domains
- latest deployment timestamp/url/stage/environment

From DNS zones:
- zone name/id/account/status/plan
- DNS records: type, name, content, proxied, ttl, id
- match records to portfolio rows by exact hostname first, then by CNAME target matching a Pages subdomain.

## Workbook shape

Start with source-data sheets:
- `Portfolio Management` — repo rows enriched with CF Pages and DNS fields.
- `Cloudflare Pages Inventory` — every Pages project, including projects bound to external GitHub owners.
- `CF External Or Unmatched` — Pages projects not matched to the target GitHub owner/repo list.
- `Cloudflare DNS Inventory` — raw DNS records.
- `Cloudflare DNS Zones` — zone summary.
- `Executive Summary` — counts and remaining gaps.

For the user's preferred SOTA/enterprise management artifact, also create an operating-system workbook layer rather than only a flat table:
- `Control Center` — portfolio counts, average completeness, P0/P1/P2/P3 operational counts.
- `Master Portfolio OS` — one row per repo with completeness score, operating priority, primary production URL, owner/account email, known risks, and next best action.
- `Action Queue` — prioritized fix list only; this is the sheet the user can operate from.
- `Relationship Matrix` — repo → GitHub → Cloudflare Pages → DNS → Lovable → Supabase → production URL.
- `Domain & URL Map` — every known URL/domain per repo, DNS zone/record/target, hosting project.
- `Supabase Matrix` — account/project/key rows with verification notes.
- `Lovable Exact Requirements` — precise remaining Lovable fields/access, not a generic request for exports.
- `Category Summary` — coverage by category: repos, avg completeness, CF/DNS/Lovable/Supabase counts.

Recommended portfolio columns:
- CF Account / Account ID
- CF Project Name
- CF Pages URL
- CF Custom Domains
- CF Repo Binding
- CF Production Branch
- CF Build Command / Output Dir / Root Dir
- CF Latest Deployment / URL / Stage / Environment
- CF Match Quality
- DNS Zone / Record Type / Record Name / Target / Proxied / TTL
- DNS Match Quality / Notes

## Remaining accuracy gaps

Cloudflare can verify Pages and DNS, but not Lovable or Supabase internals. For full repo → app → domain → database mapping, request:
- Lovable project export/session/access: project IDs, repo binding, published URL, custom domain, publish status, Supabase linkage.
- Supabase personal access token(s): project refs, names, regions/status, URLs, anon/publishable keys, org/account ownership.

Never store Cloudflare, GitHub, Lovable, or Supabase tokens in skills or memory.