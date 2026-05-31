# Lovable cookie inventory + published URL health pattern

Use when the user uploads one or more Cookie-Editor JSON exports for `lovable.dev` and wants the agent to take over project/workspace operations.

## Intake sequence

1. Treat uploaded cookie JSON as sensitive runtime input. Do not print cookie values or persist tokens in reports.
2. Parse the export and find `lovable-session-id-v2`.
3. Decode only safe JWT-like claims from the token payload for identity verification:
   - `email`
   - `name`
   - `sub` / `user_id`
   - `iat` / `exp`
   - short SHA-256 token prefix, e.g. first 12 chars, for dedupe across uploads
4. Call the authenticated Lovable API using:
   - `Authorization=[REDACTED] <lovable-session-id-v2>`
   - `Origin: https://lovable.dev`
   - `Referer: https://lovable.dev/`
   - browser-like `User-Agent`
5. Fetch `/user/workspaces` first. For every workspace, fetch projects and then project-level detail/domain/integration endpoints.
6. Save only redacted artifacts: JSON inventory + project CSV + health JSON.

## Minimum endpoints

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

## Multi-account dedupe

For each uploaded account export, compare:

- safe email/name claims
- `sub` / `user_id`
- short SHA-256 token prefix
- workspace IDs
- project IDs

If the user says “1st account / 2nd account / 3rd account,” do not assume they are distinct until these checks pass. If the export is a duplicate session, report it plainly and ask for a fresh export after switching Lovable/Google accounts.

## Published URL health check

After inventory, probe all `published_url` values with normal HTTP GET:

- status code
- final URL after redirects
- `<title>`
- timeout/error class

Flag immediately:

- `500` with app/server title: likely live app crash
- `404 Project not found`: likely unpublished, deleted, private, renamed slug, or disconnected published URL
- missing `published_url`: project may be draft/unpublished; verify with project detail and published-access endpoints

## Output contract for the user

Keep the first-account report short and evidence-first:

- confirmed identity (safe claims only)
- workspace count
- project count
- published URL count
- broken URL count and exact broken URLs
- artifact paths
- ask for the next account export

Do not overwhelm the user with every project until all accounts are merged unless they ask.