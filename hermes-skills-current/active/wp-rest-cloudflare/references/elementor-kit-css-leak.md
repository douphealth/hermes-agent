# Elementor Global CSS Leak — Detection & Fix

## What It Looks Like
CSS text visible at the top of blog posts (NOT inside `<style>` tags):
```css
.gutf-article { max-width: 100% !important; ...
```

## Root Cause
Elementor outputs the **same CSS twice** in the page `<head>`:
1. ✅ Minified inside `<style>` tags (correct)
2. ❌ Pretty-printed OUTSIDE `</style>` as a text node (the leak)

The leaking CSS (~2500 chars) becomes a visible text node in the DOM.

## Detection
Check for CSS text between `</style>` and next `<style>` in the page head:

```bash
curl -s -H "Host: gearuptofit.com" "http://ORIGIN_IP/path/" --max-time 20 | grep -oP '</style>\s*\.[a-z]+\s*\{'
```

Or via Puppeteer:
```js
const walker = document.createTreeWalker(document.head, NodeFilter.SHOW_TEXT, null, false);
let node;
while (node = walker.nextNode()) {
  if (node.textContent.includes('.gutf-article')) { /* LEAK FOUND */ }
}
```

## Where The CSS Is Stored

### Option A: `_elementor_global_css` (wp_options)
- Shows as "SERIALIZED DATA" on `wp-admin/options.php`
- Input field is `disabled` — can't edit directly
- Must use PHP `delete_option('_elementor_global_css')` or Elementor's own tools

### Option B: Elementor Active Kit Post Meta (most common for Custom CSS)
- Active kit ID stored in `elementor_active_kit` option
- Custom CSS stored as post meta `_elementor_custom_css` on the kit post
- Can clear via: Elementor → Site Settings (gear) → Custom CSS tab

### Option C: CSS Print Method
- `elementor_css_print_method` = `'external'` means Elementor writes to file
- Expected at: `wp-content/uploads/elementor/css/global.css`
- When file is 404/missing, Elementor falls back to INLINE — this is when leaks happen
- Fix: Regenerate CSS via Elementor → Tools, or delete + regenerate

## Fix Methods (in order of reliability)

### Method 1: Elementor Tools (requires wp-admin)
1. Go to Elementor → Tools
2. Click "Clear Files & Data" or "Regenerate CSS"
3. Then go to Elementor → Site Settings → Custom CSS tab
4. Delete any `.gutf-article` / `.product-box-*` rules
5. Save/Publish

### Method 2: PHP Injection (via Theme File Editor)
```php
add_action('init', function() {
    delete_option('_elementor_global_css');
    $kit_id = get_option('elementor_active_kit');
    if ($kit_id) {
        delete_post_meta($kit_id, '_elementor_custom_css');
    }
}, 1);
```
⚠️ MUST restore functions.php after execution.

### Method 3: MU Plugin via WP File Manager (best when Theme Editor reverts)
Use this when WordPress Theme Editor says: "Unable to communicate back with site to check for fatal errors, so the PHP change was reverted." That rollback is common behind Cloudflare/origin setups.

1. Login to wp-admin with Puppeteer origin mapping.
2. Open `wp-admin/admin.php?page=wp_file_manager` and wait for `window.fmfparams.nonce`.
3. Use the elFinder AJAX connector:
   - `action=mk_file_folder_manager`
   - `_wpnonce=window.fmfparams.nonce`
   - endpoint `window.fmfparams.ajaxurl`
4. Create/use `wp-content/mu-plugins/` and write a must-use plugin file, e.g. `gutf-leak-guard.php`.
5. For the Elementor plaintext leak, install an output buffer in the MU plugin that removes only:
   `</style>\s*.gutf-article ... @media (max-width: 480px) ... (?=<)`
   while preserving the valid `<style>` block.
6. Verify by fetching full files, not capped command output:
   - no `</style>\s*\.gutf-article`
   - no `</style>\s*\.[a-zA-Z0-9_-]+\s*\{`
   - the visible body start (`document.body.innerText.slice(0,2500)`) does not contain `.gutf-article`
   - real style block still present
   - no `Fatal error|Parse error|syntax error`
7. If one URL still shows the leak, check whether it is a different variant: Huawei produced the CSS as a body text node before the header/banner, not immediately after `</style>`. Broaden the guard to remove `.gutf-article` through the final mobile `@media (max-width:480px)` block in both positions while preserving valid `<style>` blocks.

**Hash examples for elFinder root on gearuptofit.com:**
- root/public_html: `l1_Lw`
- `wp-content`: `l1_d3AtY29udGVudA`
- `wp-content/mu-plugins`: `l1_d3AtY29udGVudC9tdS1wbHVnaW5z`

### Method 4: Browser Automation (Puppeteer + origin IP)
- Uses `--ignore-certificate-errors --host-resolver-rules=MAP gearuptofit.com ORIGIN_IP`
- Login via wp-login.php → navigate to Elementor Tools → Clear/Custom CSS

## Prevention
- Ensure `wp-content/uploads/elementor/css/global.css` file exists (regenerate via Elementor → Tools)
- Don't paste CSS directly into Elementor's Custom CSS field with `!important` rules everywhere
- When injecting responsive CSS, use a child theme's `style.css` or `wp-custom-css`, not post content
