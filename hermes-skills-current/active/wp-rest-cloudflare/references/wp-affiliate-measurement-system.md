# WordPress affiliate measurement + conversion module rollout

Use this when a WordPress affiliate site needs measurable monetization rather than unmanaged outbound links.

## Pattern

1. **Build a central offer registry first**
   - Source from a verified affiliate-link audit, not from a raw credential/link dump.
   - Store offer name, slug, affiliate URL, category, deployed page IDs/URLs, final URL, status, and exclusion reason for broken/mismatched links.
   - Keep credentials out of the registry.

2. **Instrument CTA anchors, not just pages**
   Add consistent metadata to every affiliate CTA:
   ```html
   data-amfs-offer="WriteSonic"
   data-amfs-offer-slug="writesonic"
   data-amfs-page-id="207939403"
   data-amfs-position="above-intro|comparison-table|mid-page|final-cta"
   data-amfs-tracking-version="YYYY-MM-affiliate-click-vN"
   rel="sponsored nofollow noopener"
   target="_blank"
   ```

3. **Emit both GA4 and GTM-compatible events**
   A site may have GA4/gtag without a GTM container. Do not block on GTM UI access if Google auth is unavailable; deploy a dual-compatible event layer:
   ```js
   window.dataLayer = window.dataLayer || [];
   dataLayer.push(Object.assign({event:'affiliate_click'}, params));
   dataLayer.push(['event','affiliate_click', params]);
   if (typeof window.gtag === 'function') window.gtag('event','affiliate_click', params);
   ```
   Event params should include: `affiliate_offer`, `affiliate_url`, `affiliate_position`, `affiliate_page_id`, `affiliate_page_url`, `affiliate_cta_text`, `affiliate_tracking_version`, plus `event_category`, `event_label`, `transport_type:'beacon'`.

4. **Conversion module structure for monetized posts**
   Put conversion elements near intent, not only at the end:
   - Above-intro disclosure + Quick verdict + Best for/Skip if + primary CTA.
   - Comparison table: `Tool | Best For | Starting Price | Key Strength | Review | Deal`; Deal buttons are tracked affiliate CTAs.
   - Mid-page CTA after pricing/pros-cons/feature/who-it-is-for sections.
   - Final CTA before conclusion with specific text (`Try WriteSonic for AI content workflows →`), not generic `Visit official website`.

5. **KPI dashboard minimum**
   Build a CSV/XLSX or Looker/Sheets dashboard with:
   - Page URL / Source post
   - Offer
   - Affiliate clicks
   - Sessions
   - Affiliate CTR = affiliate clicks / sessions
   - CTA text
   - CTA position
   - Revenue
   - EPC = revenue / affiliate clicks
   - RPM = revenue / sessions * 1000

6. **Operational monitoring**
   Create a daily link-health monitor from the central registry. Alert only on hard problems: 404/410, 5xx, closed merchant/account-state pages, or material final-destination changes. Avoid noisy alerts on harmless redirect/session parameter churn; compare normalized final host+path when possible.

## Verification contract

Before reporting success, verify all target posts with cache-busted public URLs:
- HTTP 200.
- Existing article content still visible; visible word count did not collapse.
- Above-intro, comparison-table, mid-page, and final-CTA modules present.
- CTA count and `rel="sponsored nofollow noopener"` counts are plausible.
- Every CTA has page ID, offer, position, and tracking version attributes.
- Browser-console simulated click produces an `affiliate_click` dataLayer event and, when present, calls `gtag('event','affiliate_click', params)`.
- No excluded/broken offers appear in the live CTA layer.

## Pitfalls

- Do not claim the GA4 key-event/conversion toggle was changed unless authenticated to GA4/Admin APIs or the UI was actually used. If only site-side code was changed, state that the event is firing and give the remaining GA4 Admin toggle step.
- Do not add in-page `#review` links that point to nonexistent anchors; use plain `Current guide` or create real anchors.
- Do not deploy raw affiliate links from a secrets/credential file; audit them first and exclude broken or mismatched programs.
- For WordPress behind Cloudflare/WAF, XML-RPC origin-IP edits preserve inline CSS/scripts better than REST, but back up raw post content and verify public HTML after cache-busting.
