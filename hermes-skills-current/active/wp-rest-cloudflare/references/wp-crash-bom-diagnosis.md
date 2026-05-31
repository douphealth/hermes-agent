# WordPress BOM Crash Diagnosis — Session Reference

## Session Context
Site: efficientgptprompts.com (origin IP 104.168.100.41, HostPapa/ColoCrossing, LiteSpeed + CyberPanel, Cloudflare-proxied)

## Crash Signature
- All PHP-generated URLs return `200 OK` with exactly **3 bytes** (UTF-8 BOM `\xEF\xBB\xBF`)
- Static files (readme.html, license.txt) return full content
- Intermittently, LiteSpeed cache served a stale good homepage (214KB HTML) while uncached URLs still returned BOM
- This intermittent cache behavior disappeared once the cached entry expired

## Diagnostic Commands Used

### Check if it's a PHP crash vs static file issue
```bash
# Static files work
curl -so /dev/null -w '%{http_code} %{size_download}' --resolve example.com:443:ORIGIN_IP \
  "https://example.com/readme.html"
# → 200 7425 (or similar — full content)

# PHP files crash
curl -so /dev/null -w '%{http_code} %{size_download}' --resolve example.com:443:ORIGIN_IP \
  "https://example.com/"
# → 200 3 (just the BOM)

# Same for every WordPress PHP path
curl -so /dev/null -w '%{http_code} %{size_download}' --resolve example.com:443:ORIGIN_IP \
  "https://example.com/wp-config-sample.php"
# → 500 2431 (PHP error page, PHP IS running) vs 200 3 (BOM, early startup crash)
```

### Multi-vector access check
```bash
# Check hosting panels
for port in 8090 2083 2082 8443 10000 2222 2087; do
  timeout 3 bash -c "echo > /dev/tcp/ORIGIN_IP/$port" 2>&1 && echo "Port $port OPEN" || echo "Port $port CLOSED"
done

# Check MySQL
timeout 3 bash -c "echo > /dev/tcp/ORIGIN_IP/3306" 2>&1

# Try SSH with known credentials
sshpass -p "$PASSWORD" ssh root@ORIGIN_IP "echo connected" 2>&1
```

### LiteSpeed cache identification
```bash
# Through Cloudflare proxy
curl -sI "https://example.com/" | grep -iE "x-litespeed|cf-cache-status|server|x-turbo-charged"
# → server: cloudflare
# → cf-cache-status: DYNAMIC (not cached by CF)
# → x-litespeed-purge: public,0c0_ (served from origin LSCache)

# Direct to origin
curl -sI --resolve example.com:443:ORIGIN_IP "https://example.com/" | grep -iE "x-litespeed|server"
# → server: litespeed
# → x-litespeed-cache: hit (origin LSCache served stale content)
```

## CyberPanel Access
- CyberPanel runs on port 8090 (HTTPS)
- Default login page is at `https://ORIGIN_IP:8090/`
- Login endpoint: `POST /verifyLogin` with JSON `{"username":"admin","password":"..."}`
- Redis csrf token in cookie: `csrftoken` (included in login POST as `csrfmiddlewaretoken`)
- Common default credentials: `admin/1234567`, `admin/admin`
- If Docker-based CyberPanel: the login may require `X-CSRFToken` header from the cookie value

## LiteSpeed Cache Purge (when REST is down)
```bash
# Try LiteSpeed purge via HTTP
curl -X PURGE "https://example.com/"  # May return 405
curl -H "X-LiteSpeed-Purge: *" "https://example.com/"  # Varies by config

# Through CyberPanel (if accessible)
# → LiteSpeed → Cache → Purge All
# → Or via CLI if SSH works

# Through Code Snippets (if REST works)
# Activate a snippet that calls:
#   do_action('litespeed_purge_all');
#   if (class_exists('LiteSpeed_Cache_API')) { LiteSpeed_Cache_API::purge_all(); }
```

## PHP File Access Sequence (in order of early bootstrap)
1. `.user.ini` (auto_prepend_file directive)
2. `wp-config.php`
3. `wp-content/object-cache.php`
4. `wp-content/advanced-cache.php`
5. `wp-content/mu-plugins/*`
6. `wp-content/plugins/*` (normal plugins)
7. Theme's `functions.php`

A BOM in any file loaded before #5 will crash ALL WordPress pages. A BOM in a normal plugin or theme will only break pages that load that plugin.

## Common Root Causes
1. **Nuclear restore corruption**: A shell script does `rm -rf` and downloads fresh WordPress core, but the new `wp-config.php` gets generated with BOM because the restore script's heredoc/cat output includes invisible BOM bytes
2. **`.user.ini` auto_prepend**: A PHP accelerator or security plugin creates a `.user.ini` with `auto_prepend_file` pointing to a file that has BOM
3. **Plugin update corruption**: A plugin's PHP file gets corrupted with BOM during a failed auto-update
4. **FTP upload with BOM**: A file uploaded via FTP/SFTP with UTF-8 BOM in the first bytes

## Key Headers on the Broken Site
```
server: litespeed
x-powered-by: PHP/8.x
x-litespeed-cache: hit/miss
x-litespeed-purge: public,0c0_resp,public,0c0_resp_
x-turbo-charged-by: LiteSpeed
```
