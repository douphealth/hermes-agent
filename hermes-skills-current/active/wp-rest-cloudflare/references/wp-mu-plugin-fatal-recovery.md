# WordPress MU-plugin fatal recovery after file-manager deployment

## When this applies
Use this when a WordPress production fix is deployed as an MU plugin through WP File Manager / elFinder / admin-ajax and the site immediately starts returning WordPress critical-error pages or HTTP 500.

## Key lesson
MU plugins load before normal wp-admin and before `admin-ajax.php`. If a new MU plugin has a PHP fatal, the same WordPress/WP File Manager AJAX route used to deploy it may also become unusable for rollback. Do not assume WP File Manager remains available after a bad MU-plugin write.

## Prevention gate before deploying MU-plugin PHP
1. Build the MU-plugin content locally as a `.php` file.
2. Run a syntax check before upload:
   ```bash
   php -l /path/to/plugin.php
   ```
3. Prefer the smallest possible plugin for URL-scoped changes.
4. Avoid complex quoting/regex generation directly inside Python strings without writing and linting the exact final PHP first.
5. If using output buffering for head/meta normalization, test on one non-critical path first where possible.
6. Keep the previous file content or a harmless disabled stub ready before overwriting.

## Safer deployment sequence
1. Confirm hosting-panel/SSH/FTP rollback access exists before writing any MU plugin.
2. Upload the plugin under a disabled extension first, e.g. `name.php.disabled`, if the file manager supports rename.
3. Rename to `.php` only after linting the exact content.
4. Immediately verify one cache-busted public URL.
5. If any 500 appears, rename/delete the MU-plugin file through hosting panel/SSH/FTP, not wp-admin/admin-ajax.

## Fast diagnosis
If the public site shows the generic WordPress message `There has been a critical error on this website`:

1. Probe public and origin URLs separately when Cloudflare is in front:
   ```bash
   curl -skI https://example.com/
   curl -skI -H 'Host: example.com' https://ORIGIN_IP/
   ```
2. Check whether static files still return 200. If static files work but all WordPress bootstrap routes are 500, suspect PHP fatal during bootstrap.
3. Try public debug/error files before deeper access, but never expose their contents to the user if they contain secrets:
   ```text
   /wp-content/debug.log
   /error_log
   /wp-admin/error_log
   /wp-content/error_log
   ```
4. For MU-plugin fatals, the log usually names the exact file and line, e.g. `wp-content/mu-plugins/<name>.php on line N`.

## Fast recovery
If the site is already 500 after MU-plugin deployment:
1. Do not keep retrying WordPress routes; MU load order likely blocks them.
2. Use hosting panel file manager, SSH, SFTP/FTP, or provider file access.
3. Delete or rename the bad file under:
   ```text
   public_html/wp-content/mu-plugins/<bad-plugin>.php
   ```
4. Or replace it with a harmless stub:
   ```php
   <?php
   /** Plugin Name: Disabled emergency stub */
   if (!defined('ABSPATH')) { exit; }
   ```
5. Verify homepage and a representative edited post return HTTP 200.
6. Only then revisit the head/meta issue with a linted safer plugin or plugin-native metadata repair.

## CyberPanel emergency cron fallback
When WordPress is down, wp-admin/admin-ajax is blocked, and direct SSH/FTP login fails, CyberPanel can still provide a server-side escape hatch:

1. Log in to CyberPanel. If 2FA is enabled, ask for a fresh current code and submit immediately; TOTP codes expire quickly.
2. Use the Cron UI/API for the affected domain to create a one-minute emergency cron owned by the site user.
3. Rename the fatal MU-plugin rather than editing it in place:
   ```bash
   /bin/mv /home/example.com/public_html/wp-content/mu-plugins/bad-plugin.php /home/example.com/public_html/wp-content/mu-plugins/bad-plugin.php.disabled-hermes
   ```
4. Wait for the cron interval, then verify the public homepage and `/wp-json/wp/v2/posts?per_page=1` return non-500.
5. Remove the emergency cron immediately after recovery so it does not keep running forever.
6. Download/lint/fix the disabled file offline before any re-enable attempt.

CyberPanel API pattern observed:

```text
POST /websites/getWebsiteCron  {"domain":"example.com"}
POST /websites/addNewCron      {"domain":"example.com","minute":"*","hour":"*","monthday":"*","month":"*","weekday":"*","cronCommand":"/bin/mv ..."}
```

A successful add response can look like `{"addNewCron": 1, "user": "siteuser", "cron": "* * * * * /bin/mv ..."}`. Treat that as scheduled, not as verified recovery; still perform live HTTP verification after the cron should have run.

## Reporting rule
If content was already successfully published but the site is in a 500 state from a later MU-plugin attempt, report both facts separately:
- content/database update status and backups
- current availability blocker and exact rollback file path

Do not claim the production task is done until public URLs return 200 after rollback and cache verification.
