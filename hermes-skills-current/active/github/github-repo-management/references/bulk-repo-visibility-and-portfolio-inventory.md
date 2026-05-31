# Bulk repository visibility + portfolio inventory pattern

Use this when a user asks to make all repos under a GitHub account public/private or build a management table from repo metadata.

## Bulk visibility workflow

1. Authenticate first and verify the token owner before mutating anything:
   ```bash
   curl -s -H "Authorization=[REDACTED] $GITHUB_TOKEN" https://api.github.com/user
   ```
   Confirm `.login` matches the requested owner.

2. List only repos owned by the target account. For private repos owned by the authenticated user:
   ```text
   GET /user/repos?visibility=private&affiliation=owner&per_page=100&page=N
   ```
   Filter `owner.login == TARGET` and `private == true` locally.

3. Change visibility one repo at a time:
   ```text
   PATCH /repos/{owner}/{repo}
   {"private": false}
   ```
   Treat HTTP `200` or `202` as success. Print per-repo `OK/FAIL` and continue so one failure does not hide the rest.

4. Verify with a fresh private-owned listing:
   ```text
   GET /user/repos?visibility=private&affiliation=owner&per_page=100&page=N
   ```
   Success condition: zero remaining repos where `owner.login == TARGET` and `private == true`.

5. Tell the user to revoke the temporary PAT after the operation.

## Enterprise portfolio workbook pattern

For portfolio tables, combine:
- GitHub API metadata: name, language, visibility, description, default branch, created/updated/pushed timestamps, archived/fork/topics/homepage.
- User-provided business data: category, status, product display name, Cloudflare Page, Lovable project, production URL, Supabase account/project URL/publishable key.
- Verification columns: data source, missing fields, next action.

Output an Excel workbook rather than a Telegram table when there are many columns. Good sheets:
- `Portfolio Management` — master row per repo.
- `Executive Summary` — counts and accuracy notes.
- `Needs Enrichment` — missing Cloudflare/Lovable/Supabase/domain data and exact credential/API needed.

Pitfalls:
- GitHub usernames/repo names may differ only by case or hyphenation (`mysticaldigits` vs `mystical-digits`). Normalize by repo URL/name and preserve the display/product name separately.
- The user may give stale visibility labels. Always trust live GitHub API for visibility after verifying.
- Do not store PATs in memory or skill files; use them only transiently and recommend revocation.