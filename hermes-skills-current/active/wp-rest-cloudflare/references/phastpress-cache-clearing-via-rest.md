# PhastPress Cache Clearing via REST/Temporary Code

When the PhastPress admin settings page is blocked by Cloudflare WAF or security plugins (HTTP 403), you cannot use the standard toggle-off/on cache clear method.

## Method 1: DELETE Elementor Cache (Does NOT clear PhastPress)

```bash
curl -s -X DELETE "https://site.com/wp-json/elementor/v1/cache" \
  -u "user:app_password"
```

This clears **Elementor's CSS cache** only. It does NOT clear PhastPress page cache. PhastPress caches the full rendered HTML output and serves it until its cache is explicitly cleared.

## Method 2: Temporary Cache-Clearing PHP via Theme Editor (RELIABLE)

This is the most reliable method. Write a temporary PHP action to `functions.php`, trigger it by visiting the admin URL, then remove the temporary code.

### Step 1: Add cache clearing action to functions.php

Using the theme editor programmatic access workflow (see `references/theme-editor-programmatic-access.md`), append this PHP code:

```php
// AUTO-ADDED: One-shot PhastPress cache purge
add_action('admin_init', function() {
    if (!isset($_GET['hermes_purge'])) return;
    $dirs = [
        WP_CONTENT_DIR . '/cache/phastpress',
        WP_CONTENT_DIR . '/uploads/phastpress',
        WP_CONTENT_DIR . '/phastpress',
    ];
    foreach ($dirs as $d) {
        if (!is_dir($d)) continue;
        $it = new RecursiveIteratorIterator(
            new RecursiveDirectoryIterator($d, FilesystemIterator::SKIP_DOTS),
            RecursiveIteratorIterator::CHILD_FIRST
        );
        foreach ($it as $f) {
            $f->isDir() ? @rmdir($f->getRealPath()) : @unlink($f->getRealPath());
        }
    }
    update_option('phastpress_cache_key', uniqid());
    wp_cache_flush();
    delete_transient('phastpress_cache');
    wp_redirect(remove_query_arg('hermes_purge'));
    exit;
});
```

### Step 2: Trigger the purge

```python
req = urllib.request.Request("https://site.com/wp-admin/admin.php?hermes_purge=1")
opener.open(req)
# The action fires on admin_init, deletes cache dirs, flushes WP cache, and redirects back
```

### Step 3: Remove the temporary code

Read functions.php again via the theme editor, remove the `// AUTO-ADDED` block, and save.

## Cache Directories

PhastPress may use any of these directories (created by the init hook in functions.php):
- `WP_CONTENT_DIR/cache/phastpress/`
- `WP_CONTENT_DIR/uploads/phastpress/`
- `WP_CONTENT_DIR/phastpress/`

## Verification

After clearing, verify by comparing a regular request vs a cache-busted request:

```bash
# Should show 0 matches for the buggy content
curl -s "https://site.com/page/" | grep -c "your-buggy-text"
curl -s "https://site.com/page/?phast=nocache" | grep -c "your-buggy-text"
```

Both should return the same count after cache is cleared.
