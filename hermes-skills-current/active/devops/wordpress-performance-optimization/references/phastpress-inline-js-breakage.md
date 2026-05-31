# PhastPress Inline JS Breakage: Diagnosis & Fixes

PhastPress with `scripts-defer` and `minify-inline-scripts` set `async=true` on ALL inline `<script>` elements, breaking critical page logic (scroll-reveal, counter animations, carousel init).

## Symptoms

- Hero/brand strip renders fine, then page appears blank
- All `.g-rv`, `.g-icard`, `.g-pcard` elements stay at `opacity:0`
- JS console: custom functions (`initReveal`, `boot`, etc.) are `undefined`
- HTML source contains the script, but it never executes

## Diagnosis

### Step 1: Check script elements in the rendered page

```js
// In browser console:
Array.from(document.querySelectorAll('script')).map(s => ({
    src: s.src || '(inline)',
    async: s.async,
    defer: s.defer,
    len: s.textContent.length,
    hasInitReveal: s.textContent.includes('initReveal')
})).filter(s => s.hasInitReveal || s.async)
```

If the custom script has `async: true`, PhastPress deferred it.

### Step 2: Check if functions exist

```js
typeof initReveal + ' ' + typeof boot + ' ' + typeof initCounters
// Expected: 'function function function'
// Broken:  'undefined undefined undefined'
```

### Step 3: Check PhastPress script wrapper

```js
typeof window.phast  // 'undefined' = PhastPress loader never finished
```

### Step 4: Bypass PhastPress

```bash
curl -s "https://site.com/?phast=-phast" | grep -c 'initReveal'
# Compare with normal page
curl -s "https://site.com/" | grep -c 'initReveal'
```

Both should be non-zero. If `?phast=-phast` has the script but normal page's script has `async=true`, PhastPress is the culprit.

## Fix Options (in priority order)

### Fix 1: CSS override (best for REST-only access — no code changes)

Inject CSS that forces all reveal elements visible from load:

```css
.g-rv, .g-rv-l, .g-rv-r, .g-rv-s {
    opacity: 1 !important;
    transform: none !important;
    visibility: visible !important;
}
.g-fcard { animation: none !important; }
.g-icard { opacity: 1 !important; }
```

Insert this CSS before the closing `</style>` tag in the homepage page content (see `editing-custom-pages-via-rest.md` for the technique).

**Downside:** Sacrifices scroll-reveal animations. Users prefer visible content over pretty animations that fail silently.

### Fix 1b: Re-evaluate the inline script via a delayed injection (browser-level workaround)

When you can't modify CSS, you can inject a tiny JS snippet (via page content or any injectable location) that re-evaluates the PhastPress-deferred script after a delay:

```javascript
setTimeout(function() {
    document.querySelectorAll('script').forEach(function(s) {
        if (s.textContent.includes('initReveal') || s.textContent.includes('sota-root')) {
            eval(s.textContent);
        }
    });
}, 3000);
```

**⚠️ This does NOT work reliably when injected via `elementor_snippet`.** Elementor's snippet system does not render JS code through REST API alone — the script never appears on the page. Use direct page content injection (`wp/v2/pages/{ID}`) or `functions.php` editing instead.

### Fix 2: Disable `minify-inline-scripts` in PhastPress

```bash
curl -s -b /tmp/wp_cookies.txt \
  -X POST "https://site.com/wp-admin/admin-ajax.php?action=phastpress_ajax_dispatch" \
  --data-urlencode "_wpnonce=$NONCE" \
  --data-urlencode "phast-plugins-action=save-settings" \
  --data-urlencode "phastpress-minify-inline-scripts=off"
```

Requires wp-admin session cookie + nonce (blocked by Cloudflare).

### Fix 3: Disable `scripts-defer` in PhastPress

Same endpoint as Fix 2, set `phastpress-scripts-defer=off`.

**Downside:** Reduces performance — scripts will load normally and block render.

## Root Cause

PhastPress (version 3.x) wraps every inline `<script>` in its own `window.phastScripts` array and sets `async=true` on the original element. The wrapper script (a large IIFE at page bottom) is supposed to sequentially execute deferred scripts, but when:
1. The custom script depends on `DOMContentLoaded` 
2. The PhastPress wrapper itself loads asynchronously  
3. The `DOMContentLoaded` event fires before the wrapper finishes

...the custom script's `DOMContentLoaded` listener never fires because the script wasn't loaded yet when the event occurred.

This is a known PhastPress limitation. The plugin offers no built-in exclusion list for inline scripts.
