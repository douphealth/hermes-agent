# AMFS homepage full-bleed block wrapping + render QA

Use when editing `affiliatemarketingforsuccess.com` homepage/Page ID 30 or any cache-heavy WordPress front page that is a single large custom HTML/CSS/JS landing block.

## Failure mode observed

A full custom homepage can be stored and publicly visible, but WordPress/Kadence/classic formatting may auto-insert paragraph wrappers into the `<style>` block. Public source then contains patterns like:

```html
<style>
<p>.lm-container{...}</p>
```

Symptoms:
- Raw HTML contains the redesign marker and CSS text, so string checks look successful.
- Browser DOM contains `.lumen-root`, but scoped CSS rules do not apply.
- `getComputedStyle(document.querySelector('.lm-container')).maxWidth` is `none` and container width equals viewport width.
- Runtime `<script>` guard text exists in source, but expected injected style tag (for example `#amfs-runtime-layout-guard-v23`) is absent from DOM.
- `document.querySelectorAll('style')` finds a large inline style whose `textContent` includes CSS selectors mixed with paragraph text/formatting artifacts.

This is not a design/CSS specificity problem first; it is a publication-format problem.

## Fix pattern

Publish the entire landing page as a Gutenberg Custom HTML block:

```html
<!-- wp:html -->
...full homepage HTML including <style>, markup, and <script>...
<!-- /wp:html -->
```

Do this even if XML-RPC reports success without the wrapper. XML-RPC preserving the stored string is not proof WordPress will render it as raw HTML.

## Deployment sequence

1. Backup Page ID 30 raw body via XML-RPC/REST before editing.
2. Wrap the complete landing source with `<!-- wp:html -->` and `<!-- /wp:html -->`.
3. Publish via XML-RPC when the body contains `<style>`, `@media`, or `<script>`.
4. Re-fetch the stored body and verify:
   - wrapper markers exist
   - `.lumen-root` exists
   - unique version marker exists
5. Purge/bypass caches. For AMFS, cache-busted public checks such as `?amfs_verify=<timestamp>` are required.

## Public render verification

Do not stop at source string checks. In browser console, verify:

```js
(() => {
  const c = document.querySelector('.lm-container');
  const f = document.querySelector('.lm-feat');
  return {
    root: !!document.querySelector('.lumen-root'),
    marker: document.documentElement.innerHTML.includes('AMFS runtime layout guard'),
    runtimeStyle: !!document.getElementById('amfs-runtime-layout-guard-v23'),
    containerWidth: c && getComputedStyle(c).width,
    containerMax: c && getComputedStyle(c).maxWidth,
    containerRect: c && c.getBoundingClientRect().toJSON(),
    featureGrid: f && getComputedStyle(f).gridTemplateColumns,
    overflow: document.documentElement.scrollWidth - document.documentElement.clientWidth
  };
})()
```

Pass criteria:
- `.lumen-root` exists.
- Public source and DOM have the marker.
- Runtime guard style exists if the page relies on JS-injected CSS.
- Desktop `.lm-container` max-width is constrained (target 1200px) and centered.
- Desktop featured grid is 3 columns; mobile is 1 column.
- Horizontal overflow is 0.
- CookieYes banner does not cover primary CTA/sticky CTA.

## Pitfall

If public HTML has the marker but DOM CSS is not applying, do **not** keep increasing selector specificity. First inspect `document.querySelectorAll('style')` for paragraph-wrapped CSS and republish as a `wp:html` block.