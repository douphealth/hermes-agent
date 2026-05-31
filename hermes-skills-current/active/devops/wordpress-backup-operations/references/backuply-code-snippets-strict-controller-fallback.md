# Backuply strict-controller fallback via Code Snippets REST

Use when a WordPress site needs a temporary Backuply controller/helper but normal plugin deployment is blocked by Cloudflare/wp-admin challenges, CyberPanel 2FA, or plugin upload friction, while REST application-password access and the Code Snippets plugin are available.

## Pattern

1. Keep the site in the all-site manifest as `BLOCKED` until the controller route is actually live. Do not hide it behind other running sites.
2. Discover whether Code Snippets REST exists from `/wp-json/` routes:
   - `/code-snippets/v1/snippets`
   - `/code-snippets/v1/snippets/<id>/activate`
3. Read the controller plugin PHP and convert it to snippet-safe code:
   - Remove the leading `<?php`.
   - Remove the WordPress plugin header block.
   - Keep route registration, auth checks, Backuply preparation, stop/start/tick/status endpoints, and redaction behavior.
4. Create the snippet through REST using app-password auth:
   - `POST /wp-json/code-snippets/v1/snippets`
   - Suggested fields: `name`, `desc`, `code`, `tags`, `scope=global`, `priority=1`.
5. Explicitly activate it with:
   - `POST /wp-json/code-snippets/v1/snippets/<id>/activate`
6. If activation returns a validation `500`, still immediately verify the intended route. Some installs may create/load the code despite a REST activation validation error, or the route may already be live from a prior activation.
7. Verify the controller route directly before starting backups:
   - `/wp-json/hermes-backuply-strict/v1/status?...`
   - Require `backuply_active=true`, remote location visible, DB/files settings true, and no root `wp-content/uploads` exclusion.
8. Start a dedicated runner for the formerly blocked site if the main fleet runner is sequentially busy. This is acceptable when hosts/paths differ and the user asked for ASAP full backups.

## Reporting discipline

- Do not paste raw route dumps or long diagnostic JSON to the user. Summarize as terse status labels: `FIXED_ROUTE`, `RUNNING_STRICT_FULL`, `BLOCKED`, `FAILED`, `VERIFIED_FULL`.
- Raw route dumps belong in local logs/reference notes only.
- If the user reacts with frustration (`Wtf is this?`), immediately acknowledge the raw diagnostic was inappropriate, summarize the actionable result, and continue executing.

## Verification before green

A Code Snippets-deployed controller is only an access-channel fix. The backup remains incomplete until the fresh Backuply artifact passes the normal strict-full checks:

- Fresh same-site artifact.
- DB + files flags present.
- Root uploads not excluded.
- Size plausible versus current uploads inventory and/or historical full artifacts.
- Remote location matches intended Google Drive target.
