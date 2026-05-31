# Lovable portfolio enrichment without OAuth

Use this when building an enterprise portfolio table that cross-links GitHub repos, Cloudflare Pages/DNS, Lovable projects, published apps, and Supabase.

## User/workflow lesson

Do **not** start by asking the user to manually export Lovable projects/screenshots if public/API inference has not been exhausted. For this user, over-asking manual Lovable work is a failure mode. First create or update a useful artifact from all accessible sources, then ask only for the smallest private access needed.

## Public-first workflow

1. Start from existing repo/app workbook rows and collect candidate Lovable URLs from fields such as `Lovable App`, `Website URL`, `Cloudflare Page`, `CF Pages URL`, and DNS records.
2. Probe known `https://lovable.dev/projects/<uuid>` URLs with a browser-like User-Agent.
   - `HTTP 200` + title `Login` means the project URL exists, but private dashboard metadata is behind Google OAuth.
   - Record this as evidence, not as a failure.
3. Probe public `*.lovable.app` URLs.
   - Capture HTTP status, final URL, `<title>`, meta description, public GitHub links, and public Supabase URLs if exposed in rendered HTML.
4. Search Cloudflare DNS records for Lovable clues:
   - TXT names like `_lovable.example.com` or `_lovable.www.example.com`
   - TXT values like `lovable_verify=...`
   - CNAMEs/targets containing `lovable`
5. Merge all evidence back into the workbook before asking for login/session access.

## Fields to add to the workbook

Add columns such as:

- `Lovable Project URL Status`
- `Lovable Project Page Title`
- `Lovable Public Access Result`
- `Lovable Published App Status`
- `Lovable Published App Title`
- `Lovable Public GitHub Links Found`
- `Lovable Public Supabase URLs Found`
- `Lovable Verification DNS Clues`
- `Lovable Confidence`
- `Lovable Notes`

Add sheets such as:

- `Lovable Public Probe`
- `Lovable DNS Clues`
- `Lovable Exact Requirements`

## Exact private Lovable data still needed

Only after public enrichment is complete, ask for one of:

1. Lovable workspace invite link. Prefer role `editor` for inventory because `viewer` may hide integrations, GitHub binding, domains, Supabase settings, and environment variable names. If the user is risk-sensitive, start with `member`/`viewer`, then escalate only if settings are hidden.
2. Temporary collaborator account.
3. Authenticated browser/session cookies for `lovable.dev`.
4. Screenshots/video of project/settings pages as a last resort.

### Workspace invite-link flow

When the user provides `https://lovable.dev/workspace-invite/<uuid>` links, immediately open one with the browser. Current Lovable behavior redirects anonymous users to `https://lovable.dev/login?redirect=/workspace-invite/<uuid>`; the link itself is valid but cannot be accepted without a logged-in Lovable user. Do **not** ask the user to export projects at this point.

Ask for exactly one temporary Lovable account/session to accept all invite links:

- If the user already accepted the invites with a temporary account, ask only for a way to authenticate that temporary account in the agent browser: magic link, session cookies, or Google approval/password/2FA as appropriate.
- If not accepted yet, ask them to log in once with the temporary account and accept each invite link, or provide the magic link/session so the agent can accept the invites.
- Explain in one sentence: "The invite links invite an account; I have the invitations, but I need the invited logged-in account/session to open the private workspace."

Avoid repeating long option lists after the user is frustrated. Give the single next required item.

Ask for these exact dashboard fields per project:

- Lovable account/workspace owner email
- Project name
- Project UUID
- Project URL
- Published `*.lovable.app` URL
- Custom domain
- Connected GitHub repo
- GitHub sync/reconnect status
- Publish/deployment status
- Last published/updated time
- Connected Supabase project/ref/URL if shown
- Environment variable names only, never secret values
- Duplicate/deprecated status if visible

## Reporting rule

Phrase the remaining blocker precisely: "Public Lovable evidence is enriched; private dashboard-only fields require an authenticated Lovable session or workspace invite." Do **not** imply the user must manually build the table.