# Lovable multi-invite/session handling reference

Use this when a user is building a SaaS/project inventory and Lovable OAuth blocks direct agent login.

## Proven flow

1. User creates Lovable workspace invite links for each target workspace.
2. User accepts those invites with a temporary Lovable/Google account.
3. User exports Cookie-Editor JSON while on `https://lovable.dev/projects`.
4. Agent extracts `lovable-session-id-v2` and calls `https://api.lovable.dev` with `Authorization=[REDACTED] <token>`.
5. Agent fetches `/user/workspaces`, workspace project lists, project detail/domain/integration/repo-accessibility endpoints, and workspace Supabase orgs.
6. Agent merges only newly discovered workspace/project IDs into the workbook.

## UX lesson from the session

The phrase “session cookie/export” confused the user. When this happens, stop abstract wording immediately and give one concrete action:

> Open Lovable in Chrome as `<temporary_email>`, go to projects, click Cookie-Editor, Export JSON, upload the file here.

Avoid explaining OAuth mechanics unless asked.

## Deduping multiple uploaded cookie files

Multiple files may be labeled as different Lovable accounts but still authenticate as the same temporary account. Before merging:

- Decode only safe JWT payload fields from `lovable-session-id-v2` without printing the token=[REDACTED] `name`, `sub`/`user_id`, `iat`, `exp`.
- Compare a short SHA-256 token prefix for diagnostic identity only.
- Fetch and compare workspace IDs and project IDs.
- If identical, report no workbook delta.
- If a later cookie reveals additional accepted workspaces, rebuild the workbook and report exact added workspace/project deltas.

## Observed useful delta report format

- Authenticated account: `<email>`
- Workspaces visible: `<n>`
- Projects pulled: `<n>`
- New workspace IDs: `<n>`
- New project IDs: `<n>`
- Added projects: name, GitHub owner/repo if visible, published URL

This keeps the reply concrete and avoids re-litigating access mechanics.