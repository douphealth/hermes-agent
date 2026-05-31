# MainWP local dashboard site connection repair

Use this when a WordPress child site appears offline or disconnected in a local MainWP dashboard even though the public site is reachable and the MainWP Child plugin is installed.

## Diagnostic pattern

1. Public child-site probes first:
   - `https://example.com/` should return 200.
   - `https://example.com/wp-json/` should return 200 unless intentionally blocked.
   - `https://example.com/wp-content/plugins/mainwp-child/readme.txt` returning 200 is strong evidence the MainWP Child plugin exists on the child site.
   - `https://example.com/wp-admin/admin-ajax.php` returning bare `0`/400 without POST data is normal; it means WordPress AJAX is present, not that MainWP works.
2. Check child WordPress admins by logging into the child site with stored WP-admin credentials and visiting `wp-admin/users.php?role=administrator`. MainWP needs its stored `adminname` to match a real administrator username on the child site.
3. Inspect the local MainWP dashboard DB tables:
   - `wp_mainwp_wp`: site row, `adminname`, `url`, `http_response_code`, `ip`, keys.
   - `wp_mainwp_wp_sync`: `sync_errors`, `dtsSync`, `dtsSyncStart`, version/health.
   - `wp_mainwp_action_log`: current/recent MainWP request traces.

## Local by Flywheel / LocalWP database access pattern

For LocalWP sites, the MySQL config is usually under:

- `C:/Users/<User>/AppData/Roaming/Local/run/<site-id>/conf/mysql/my.cnf`

That file exposes the port/user/password. In WSL, use the bundled Windows MySQL client, for example:

```bash
MYSQL='/mnt/c/Users/<User>/AppData/Roaming/Local/lightning-services/mysql-8.4.0/bin/win64/bin/mysql.exe'
"$MYSQL" -h 127.0.0.1 -P <PORT> -uroot -proot local -e "SELECT id,url,name,adminname,http_response_code,ip FROM wp_mainwp_wp WHERE url LIKE '%example.com%'; SELECT * FROM wp_mainwp_wp_sync WHERE wpid=<ID>\\G;"
```

Always back up the target rows before updating:

```bash
"$MYSQL" -h 127.0.0.1 -P <PORT> -uroot -proot local -N -B -e "SELECT * FROM wp_mainwp_wp WHERE id=<ID>; SELECT * FROM wp_mainwp_wp_sync WHERE wpid=<ID>;" > ~/mainwp-example-before-$(date +%Y%m%d-%H%M%S).sql
```

## Common fix: stored admin username no longer exists

Symptom in `wp_mainwp_wp_sync.sync_errors`:

```text
ERROR: Unexisting administrator user. Please verify that it is an existing administrator.
```

Fix by replacing the dashboard-side MainWP `adminname` with an actual child-site administrator username and clearing the stale sync error:

```sql
UPDATE wp_mainwp_wp
SET adminname='Admin'
WHERE id=<ID> AND url='https://example.com/';

UPDATE wp_mainwp_wp_sync
SET sync_errors=''
WHERE wpid=<ID>;
```

Then trigger a sync from the local dashboard code if possible. With LocalWP PHP, load the site with the matching `php.ini` so mysqli is enabled:

```bash
PHP='/mnt/c/Users/<User>/AppData/Roaming/Local/lightning-services/php-8.3.0+1/bin/win64/php.exe'
INI='C:/Users/<User>/AppData/Roaming/Local/run/<site-id>/conf/php/php.ini'
"$PHP" -c "$INI" -r '
define("WP_USE_THEMES", false);
require "C:/Users/<User>/Local Sites/<local-site>/app/public/wp-load.php";
use MainWP\Dashboard\MainWP_DB;
use MainWP\Dashboard\MainWP_Sync;
$w = MainWP_DB::instance()->get_website_by_id(<ID>);
$ret = MainWP_Sync::sync_site($w, true, true, true);
var_export($ret);
echo PHP_EOL;
'
```

Expected result: `true`, `wp_mainwp_wp_sync.sync_errors` remains empty, and `dtsSync` advances.

## Pitfalls

- Do not assume a public `xmlrpc.php` 403 is the MainWP failure. MainWP normally talks to the child via `wp-admin/admin-ajax.php` and signed MainWP Child payloads.
- Do not rewrite the MainWP RSA keys unless the dashboard explicitly requires reconnection. First verify the stored admin username and current sync error.
- LocalWP CLI PHP without the site `php.ini` may miss `mysqli` and WordPress will show “Your PHP installation appears to be missing the MySQL extension.” Use the LocalWP run `conf/php/php.ini` with the matching bundled PHP binary.
- MainWP action logs may be stale if the LocalWP site has been paused for a long time; trust the current DB row and a fresh sync result over old 2024 log timestamps.
