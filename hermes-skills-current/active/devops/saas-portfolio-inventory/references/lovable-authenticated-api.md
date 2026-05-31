# Lovable authenticated API reference

Condensed from a successful authenticated Lovable inventory run. Do not store actual cookie/session values here.

## Best access path

1. User creates/uses a temporary Lovable/Google account.
2. User accepts all Lovable workspace invite links while logged in.
3. User opens `https://lovable.dev/projects`.
4. User exports **only** `lovable.dev` cookies as Cookie-Editor JSON.
5. Agent reads the uploaded JSON, extracts `lovable-session-id-v2`, and calls Lovable API with it as a bearer token.

If the user is confused, ask for exactly this single next item:

```text
Upload the Cookie-Editor JSON export from lovable.dev after logging in as the temporary account and accepting the invite links.
```

## Request headers

```text
Authorization=[REDACTED] <lovable-session-id-v2>
Origin: https://lovable.dev
Referer: https://lovable.dev/
Accept: application/json
User-Agent: Mozilla/5.0
```

Do not log or print `<lovable-session-id-v2>`.

## Useful endpoints

Base: `https://api.lovable.dev`

- `/user/workspaces`
- `/user/workspace-invitations`
- `/workspaces/{workspace_id}`
- `/workspaces/{workspace_id}/projects?limit=250`
- `/workspaces/{workspace_id}/projects/draft?limit=250`
- `/workspaces/{workspace_id}/supabase-organizations`
- `/projects/{project_id}/details`
- `/projects/{project_id}/domains`
- `/projects/{project_id}/integrations`
- `/projects/{project_id}/repo-accessibility`
- `/projects/{project_id}/workspace`
- `/workspaces/{workspace_id}/projects/{project_id}/published-access`

Observed non-useful/404 endpoints can vary; don't encode failures as permanent assumptions.

## Fields to flatten

Project-level:

- `id`, `workspace_id`, `name`, `display_name`
- `url`, `is_published`, `published_at`, `publish_visibility`, `visibility`
- `github_owner.name`, `github_repo_name`, `github_repo_id`, `is_github`
- `status`, `tech_stack`, `main_branch`, `latest_commit_sha`, `preview_build_commit_sha`
- `last_edited_at`, `updated_at`, `created_at`
- `edit_count`, `user_message_count`, `credit_total`
- `published_deployment.status`, `.target_name`, `.branch`, `.commit_sha`
- `latest_screenshot_url`, `generated_description`, `description`

Extra API calls:

- `/domains`: list custom domains and status.
- `/integrations`: may expose `supabase`, `memory`, `ai_gateway`.
- `/repo-accessibility`: e.g. `repo_accessible`.
- `/supabase-organizations`: Supabase org/project/region/status/database metadata visible from Lovable.

## Redaction rules

- Never persist cookie/session values.
- Supabase `publishable_key` or anon-like keys may appear in `/integrations`; include only when explicitly needed. Prefer redacting in deliverables unless the user requested operational key inventory.
- Do not place tokens or uploaded cookie file contents in skills, memories, or final responses.

## Verification counts to report

- workspaces visible
- pending invites
- Lovable projects pulled
- Lovable projects matched into portfolio
- unmatched Lovable projects
- Supabase org/project connections visible via Lovable
- workbook path, CSV path, sheet count, master row/column count
