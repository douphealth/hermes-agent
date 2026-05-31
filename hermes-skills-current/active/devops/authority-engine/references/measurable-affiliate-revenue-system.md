# Measurable Affiliate Revenue System for WordPress

Use this when the user asks to move beyond affiliate link insertion into an enterprise-grade, measurable monetization system.

## Goal
Turn scattered affiliate CTAs into a measurable revenue system with:
- a central offer registry
- instrumented live CTA buttons
- GTM/GA4-compatible click events
- page/offer/CTA attribution
- daily affiliate link health monitoring
- verification artifacts proving the live pages emit events

## Preconditions
- A verified affiliate offer table exists, with broken/missing offers excluded.
- High-intent posts already have or will receive affiliate CTA modules.
- WordPress write access is available through REST or XML-RPC; use XML-RPC when REST write is blocked or strips HTML/script/style.

## Implementation pattern

### 1. Build the central registry
Create a JSON registry outside the post body, e.g. `/home/hermes/<site>_affiliate_registry.json`:

```json
{
  "site": "example.com",
  "measurement_version": "YYYY-MM-affiliate-click-v1",
  "event_name": "affiliate_click",
  "required_link_rel": "sponsored nofollow noopener",
  "offers": [
    {
      "offer": "WriteSonic",
      "slug": "writesonic",
      "category": "AI writing",
      "url": "https://...",
      "status": "active_public_verified",
      "http_status": 200,
      "final_url": "https://...",
      "tracking_marker_status": "YES: via=...",
      "last_public_verified_at": "YYYY-MM-DD"
    }
  ],
  "deployed_pages": [
    {"post_id": 123, "url": "https://example.com/post/", "offers": ["WriteSonic", "Jasper"]}
  ],
  "missing_or_not_deployed": [],
  "excluded_broken": []
}
```

Do not store credentials in the registry.

### 2. Add tracking attributes to CTA links
Each live affiliate CTA anchor should include:

```html
<a class="amfs-affiliate-btn"
   href="https://affiliate.example/"
   target="_blank"
   rel="sponsored nofollow noopener"
   data-amfs-offer="WriteSonic"
   data-amfs-offer-slug="writesonic"
   data-amfs-page-id="123"
   data-amfs-position="affiliate-box"
   data-amfs-tracking-version="YYYY-MM-affiliate-click-v1">Try WriteSonic →</a>
```

Use a site-specific prefix for data attributes if not AMFS. Keep `rel="sponsored nofollow noopener"` mandatory.

### 3. Add a lightweight event tracker
Append one tracker script per edited post/body, or deploy once globally if safe. The script should emit both object-style and gtag-compatible events:

```html
<script data-affiliate-click-tracker="YYYY-MM">
(function(){
  if (window.__affiliateTrackerV1) return;
  window.__affiliateTrackerV1 = true;
  function clean(s){return (s||'').toString().replace(/\s+/g,' ').trim().slice(0,180);}
  function params(a){
    return {
      event_category: 'affiliate',
      event_label: clean(a.getAttribute('data-amfs-offer') || a.textContent),
      affiliate_offer: clean(a.getAttribute('data-amfs-offer') || a.textContent.replace(/^Try\s+/i,'')),
      affiliate_url: a.href,
      affiliate_position: a.getAttribute('data-amfs-position') || 'affiliate-box',
      affiliate_page_id: a.getAttribute('data-amfs-page-id') || '',
      affiliate_page_url: location.href.split('#')[0],
      affiliate_cta_text: clean(a.textContent),
      affiliate_tracking_version: 'YYYY-MM-affiliate-click-v1',
      transport_type: 'beacon'
    };
  }
  document.addEventListener('click', function(e){
    var a = e.target && e.target.closest ? e.target.closest('a.amfs-affiliate-btn') : null;
    if (!a) return;
    var p = params(a);
    window.dataLayer = window.dataLayer || [];
    window.dataLayer.push(Object.assign({event:'affiliate_click'}, p));
    window.dataLayer.push(['event','affiliate_click', p]);
    if (typeof window.gtag === 'function') window.gtag('event','affiliate_click',p);
  }, true);
})();
</script>
```

If the site uses a different CTA class, adjust the selector. Prefer global deployment only when it will not affect layout/performance; otherwise use scoped post-body insertion with backups.

### 4. Verify live behavior
Automated verification for every instrumented page:
- HTTP 200
- exactly one tracking script/version marker
- at least one affiliate CTA button
- `data-*` offer/page attributes present
- `rel="sponsored nofollow noopener"` count >= expected offers
- expected offer names visible
- excluded broken URLs/patterns absent

Browser proof on at least one representative page:

```js
(() => {
  const a=document.querySelector('a.amfs-affiliate-btn');
  const before=(window.dataLayer||[]).length;
  a.dispatchEvent(new MouseEvent('click',{bubbles:true,cancelable:true,view:window}));
  return (window.dataLayer||[]).slice(before);
})()
```

Expected result includes an `affiliate_click` object with `affiliate_offer`, `affiliate_url`, `affiliate_page_id`, and `affiliate_tracking_version`.

### 5. Configure GTM/GA4
If GTM is not already forwarding custom events:
- GTM Trigger: Custom Event, name `affiliate_click`
- GA4 Event Tag: event name `affiliate_click`
- Parameters: `affiliate_offer`, `affiliate_url`, `affiliate_position`, `affiliate_page_id`, `affiliate_page_url`, `affiliate_cta_text`, `affiliate_tracking_version`

Do not claim GA4 reporting is complete unless the console/tag configuration is verified or the browser network confirms GA4 receives the event.

### 6. Add daily link-health monitoring
Create a monitor script that reads the registry and checks active offers. Alert only on material failures:
- 404/410
- 5xx
- closed merchant/inactive merchant page
- account-state/error final URL
- material final-path change
- tracking marker disappearance when reliably detectable

Avoid noisy alerts from dynamic query params (`clickid`, `sscid`, `ps_xid`) or bot-protection 403s if the final host/path remains materially correct.

Normalize final destination using host + path, not full query string, for change detection.

## Pitfalls
- Public URL resolution is not commission-grade proof. Dashboard-side click attribution still needs manual or API confirmation.
- Do not use inactive/closed/mismatched links just because they return HTTP 200.
- REST may strip `<script>`/`<style>` or block writes; use XML-RPC with backups when needed.
- If a click opens a new tab, browser-testing may navigate away; dispatch synthetic click events or use ctrl/meta click and inspect `dataLayer` immediately.
- GTM may also emit `gtm.linkClick`; this is not a replacement for the custom `affiliate_click` event.
- Be careful with monitor body-text checks: generic strings like `404` can appear in legitimate pages/scripts. Prefer specific merchant error phrases and final URL patterns.

## Output contract
Report:
- registry path and active offer count
- pages instrumented
- verification pass/fail count
- sample browser proof event
- monitor script path and schedule/job ID
- remaining blocked step: dashboard attribution and/or GTM→GA4 console mapping if not verified
