# MainWP Backuply control-plugin deployment pattern

Use this when a Backuply fleet repair depends on deploying or updating a small helper/control plugin through MainWP before running backups.

## Durable lessons

- **Prove the delivery artifact before redeploying.** If the helper ZIP is served through a tunnel/static HTTP directory, hash the local ZIP and the remotely fetched URL. A successful MainWP install can still install stale code if the served file was not overwritten.
- **Resolve exact MainWP child IDs from the MainWP database/list immediately before action.** Do not rely on remembered IDs; stale site-ID maps can silently deploy to the wrong child site.
- **Verify helper version from the child site after deployment.** A MainWP `results[zip]=true` only proves the package was accepted. Call the helper status/runtime endpoint on each child and require the expected version and endpoint behavior before running destructive/reset backup actions.
- **For LocalWP-backed MainWP automation, run PHP with the matching Local runtime `php.exe` and its active `php.ini`.** The useful pattern is not “PHP was missing mysqli”; it is to pair the exact LocalWP PHP version with the generated runtime php.ini so mysqli/extensions load correctly.
- **After deploying a new Backuply control helper, run `prep` before `start`.** Prep should reset stale Backuply status, set the validated remote location, and apply safe excludes before a fresh artifact-only backup.

## Minimum verification chain

1. List MainWP sites: id, name, url.
2. Hash local helper ZIP and remotely served helper ZIP; require match.
3. MainWP install/update package to exact child IDs.
4. Query child helper status/runtime endpoint; require expected helper version.
5. Call prep with intended Backuply remote location.
6. Query status again; require location and excludes are active.
7. Only then start/tick Backuply and wait for fresh same-site backup-info artifact.

## Backuply huge-site excludes to include during prep

- `wp-content/backuply/backups`
- `wp-content/cache`
- `wp-content/wphb-cache`
- `wp-content/et-cache`
- `wp-content/litespeed`
- `wp-content/wp-rocket-config`
- `wp-content/ai1wm-backups`
- `wp-content/updraft`
- `wp-content/upgrade`
- `wp-content/debug.log`
- `wp-content/uploads/ShortpixelBackups`
- lowercase/variant optimizer backup directories where present
- log/tmp extensions

## Reporting

Keep urgent ops output terse: `DEPLOYED`, `PREPPED`, `RUNNING`, `VERIFIED`, `FAILED`, or `BLOCKED`. Never call a Backuply backup successful until a fresh same-site artifact appears.