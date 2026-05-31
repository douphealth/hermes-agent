# MainWP on LocalWP: child-site connection and OpenSSL warning repair

Use when MainWP Dashboard runs in LocalWP on Windows (e.g. `C:\Users\Admin\Local Sites\...`) and a child WordPress site will not connect/sync, or `managesites` shows PHP OpenSSL warnings.

## Fast diagnosis

1. Locate the LocalWP site files under `/mnt/c/Users/<user>/Local Sites/<site>/app/public/` from WSL.
2. Read `wp-config.php` for DB settings. LocalWP usually uses `DB_NAME=local`, `DB_USER=root`, `DB_PASSWORD=[REDACTED]
3. Find the live LocalWP MySQL port in:
   - `/mnt/c/Users/<user>/AppData/Roaming/Local/run/<site-id>/conf/mysql/my.cnf`
   - Example: `port = 10014`
4. Use LocalWP's bundled `mysql.exe` from WSL to query the dashboard DB:
   ```bash
   MYSQL='/mnt/c/Users/Admin/AppData/Roaming/Local/lightning-services/mysql-8.4.0/bin/win64/bin/mysql.exe'
   "$MYSQL" -h 127.0.0.1 -P 10014 -uroot -proot local -e "SELECT id,url,name,adminname,http_response_code,ip FROM wp_mainwp_wp;"
   ```

## Child site shows disconnected / sync error

Check the site row and sync table:

```sql
SELECT id,url,name,adminname,http_response_code,ip FROM wp_mainwp_wp WHERE url LIKE '%example.com%';
SELECT * FROM wp_mainwp_wp_sync WHERE wpid=<site_id>\G;
```

If `sync_errors` says:

`ERROR: Unexisting administrator user. Please verify that it is an existing administrator.`

then MainWP's stored `adminname` is not an actual administrator username on the child site.

Verify the child site's actual admin users by logging in or authenticated wp-admin request, then update MainWP:

```sql
UPDATE wp_mainwp_wp SET adminname='Admin' WHERE id=<site_id>;
UPDATE wp_mainwp_wp_sync SET sync_errors='' WHERE wpid=<site_id>;
```

Run a MainWP sync from the LocalWP PHP runtime:

```bash
PHP='/mnt/c/Users/Admin/AppData/Roaming/Local/lightning-services/php-8.3.0+1/bin/win64/php.exe'
INI='C:/Users/Admin/AppData/Roaming/Local/run/<site-id>/conf/php/php.ini'
"$PHP" -c "$INI" -r '
define("WP_USE_THEMES", false);
require "C:/Users/Admin/Local Sites/mywebsites/app/public/wp-load.php";
$w=\MainWP\Dashboard\MainWP_DB::instance()->get_website_by_id(<site_id>);
$ret=\MainWP\Dashboard\MainWP_Sync::sync_site($w,true,true,true);
var_export($ret);
'
```

`true` means MainWP connected.

## `openssl_pkey_export(): Cannot get key from parameter 1`

Symptom on MainWP pages:

`Warning: openssl_pkey_export(): Cannot get key from parameter 1 in .../mainwp/pages/page-mainwp-server-information-handler.php on line 239`

Root cause pattern:

- `mainwp_opensslLibLocation` points to a non-existent Windows path, commonly `C:\php\extras\ssl\openssl.cnf`.
- MainWP calls `openssl_pkey_new()` with the stale config path, receives `false`, then calls `openssl_pkey_export(false, ...)`, producing the visible warning.

Diagnose:

```bash
PHP='/mnt/c/Users/Admin/AppData/Roaming/Local/lightning-services/php-8.3.0+1/bin/win64/php.exe'
INI='C:/Users/Admin/AppData/Roaming/Local/run/<site-id>/conf/php/php.ini'
"$PHP" -c "$INI" -r '
define("WP_USE_THEMES", false);
require "C:/Users/Admin/Local Sites/mywebsites/app/public/wp-load.php";
echo get_option("mainwp_opensslLibLocation").PHP_EOL;
$conf=["private_key_bits"=>2048];
$loc=\MainWP\Dashboard\MainWP_System_Utility::get_openssl_conf();
if($loc) $conf["config"]=$loc;
var_dump($conf, openssl_pkey_new($conf));
while(($e=openssl_error_string())!==false) echo "ERR:$e\n";
'
```

Repair options:

1. Set OpenSSL config to the real LocalWP PHP file:
   ```php
   update_option('mainwp_opensslLibLocation', 'C:/Users/Admin/AppData/Roaming/Local/lightning-services/php-8.3.0+1/bin/win64/extras/ssl/openssl.cnf');
   ```
2. If Windows OpenSSL continues to emit noisy errors even with a valid config, set MainWP's global verification method to PHPSECLIB fallback:
   ```php
   update_option('mainwp_verify_connection_method', 2);
   ```
   In MainWP this displays as `PHPSECLIB (fallback)` and makes `get_ssl_warning()` return empty.
3. Defensive plugin patch for local-only MainWP installs: guard `openssl_pkey_export()` in `page-mainwp-server-information-handler.php` so it only runs when `openssl_pkey_new()` returns a key, and suppress the warning consistently with the nearby `get_openssl_working_status()` method:
   ```php
   $res = openssl_pkey_new( $conf );
   if ( false !== $res ) {
       @openssl_pkey_export( $res, $privkey, null, $conf );
   }
   ```

## Verification

- `php -l page-mainwp-server-information-handler.php` passes.
- `MainWP_Server_Information_Handler::get_ssl_warning()` returns empty if PHPSECLIB fallback is enabled.
- `MainWP_Server_Information_Handler::get_openssl_working_status()` returns true.
- `MainWP_Sync::sync_site($website, true, true, true)` returns true for the repaired child site.
- Fetch `http://localhost:<port>/wp-admin/admin.php?page=managesites` from Windows/PowerShell and confirm no `openssl_pkey_export`, `Cannot get key`, or `page-mainwp-server-information-handler.php` warning appears.

## Pitfalls

- WSL `localhost:<LocalWP port>` may fail even when Windows `localhost:<port>` works. Use `powershell.exe Invoke-WebRequest` for Windows-local verification instead of concluding the site is down.
- Do not store or print WordPress/hosting credentials. Parse local secret files only inside scripts and redact output.
- Before direct DB changes, dump the relevant `wp_mainwp_wp` and `wp_mainwp_wp_sync` rows to a timestamped backup file.
- Plugin source patches can be overwritten by MainWP updates; prefer settings (`mainwp_opensslLibLocation`, `mainwp_verify_connection_method`) first, patch only to suppress visible warnings on local dashboards.