# Cloudflare Pages and DNS Cross-Account Inventory Pattern

Use when a user supplies Cloudflare API tokens for portfolio/app inventory.

## Key lesson

Cloudflare Pages projects and DNS zones may live under different Cloudflare accounts/emails.

A token can be valid and have correct read permissions but still return:

```json
{"success": true, "result": [], "result_info": {"total_count": 0}}
```

for `/zones`. This is not necessarily a permission failure. If `/accounts` and `/accounts/{id}/pages/projects` work but `/zones` returns zero, the likely cause is: Pages are in one Cloudflare account and DNS zones are in another.

## Verification sequence

1. Verify token:
   - `GET /user/tokens/verify`
2. List accounts:
   - `GET /accounts`
3. List Pages projects for each account:
   - `GET /accounts/{account_id}/pages/projects?page=1`
   - Pages API may reject `per_page=50/100` with `Invalid list options`; page with default `per_page=10`.
4. List zones:
   - `GET /zones?per_page=50`
5. If zones are zero, test known domains explicitly:
   - `GET /zones?name=example.com`
6. If still zero, ask for a token from the Cloudflare account that owns DNS zones, not for more permissions on the Pages-only account.

## Data to capture

Pages project fields:
- account name/id
- project name
- `*.pages.dev` subdomain
- custom domains
- source repo binding (`source.config.owner`, `source.config.repo_name`)
- production branch
- build command, root directory, output directory
- latest deployment timestamp/url/environment/stage

DNS fields:
- zone name/id/account
- record type/name/content/proxied/TTL
- map exact hostname from Website URL / Cloudflare custom domains first
- then map CNAME targets to `*.pages.dev`

## User communication

If the user shows a screenshot proving the token has `Zone:Zone Read` and `Zone:DNS Read`, do not repeat that they need those permissions. Say the token is configured correctly and explain the account split: Pages account works, DNS zones are under another account/email.
