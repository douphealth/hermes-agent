# WordPress affiliate revenue recovery playbook

Use when the user asks for revenue-critical affiliate fixes after an affiliate measurement rollout. Focus on public trust, measurable clicks, and page-level revenue attribution — not more infrastructure.

## Scope discipline
- Do **not** add new infrastructure unless required to restore tracking/revenue.
- Work on the live public surface: logged-out pages, cache-busted URLs, raw HTML, and rendered/parsed DOM.
- Be explicit when a step requires external admin access (GA4/GTM UI, affiliate dashboards) and do the site-side equivalent immediately.

## Public verification contract
For every monetized URL, verify as a logged-out user with both raw HTML and a rendered or parsed DOM check:
- `.amfs-affiliate-box`
- `data-amfs-offer`
- `data-amfs-position`
- `rel` contains `sponsored`
- `affiliate_click` appears in the tracker
- above-intro CTA is visibly present near the top of article content

If any check fails:
1. Patch the post via XML-RPC/origin bypass.
2. Purge WordPress/plugin/CDN cache where credentials allow.
3. Re-run the same public verification until it passes.

## Trust cleanup
Remove or rewrite fake, future-dated, or unverifiable claims before optimizing conversions. Common high-risk patterns:
- `Q4 2026`, `Q1 2026` when used as completed tests/studies/data.
- `847 live sites` or similar exact-sounding unverifiable sample claims.
- Fake/unverifiable studies, surveys, benchmarks, lab names, or unsupported percentages.
- Claims like `n=2,847`, `n=1,500 sites`, `500+ workflows` unless a real citation/source exists in the page.

Log removed snippets by URL. After editing, search public HTML with scripts/styles stripped so valid schema/scripts do not cause false positives.

## Affiliate sub-ID tracking
Add sub-ID/campaign tracking to affiliate CTAs only where safely supported by the affiliate/network URL. Format:

```text
page_id_offer_slug_CTA_position
```

Example:

```text
207939403_writesonic_above-intro
```

Useful parameter patterns observed:
- ShareASale: `afftrack`
- FirstPromoter/FPR style links (`fpr=`, `fp_ref=`): `fp_sid`
- Generic `via=` SaaS links: often `sub_id`
- Pictory/WordPress/Bluehost/WPX-style links: often `subid`
- AWeber/GetResponse-style links: `custom`
- SiteGround: `campaign`
- Vultr: `ref_subid`
- Kinsta: `ka_subid`

Do **not** force arbitrary params onto opaque/private redirect paths where attribution could break (e.g. some PartnerStack, app redirect, promo-code, or path-token links). Record these as `not_supported_or_opaque` instead of pretending coverage is 100%.

## GA4/GTM handling
If the site already has GA4 `gtag` but no usable GTM/admin auth:
- Fire `affiliate_click` site-side through both `gtag('event', ...)` and `dataLayer.push({event:'affiliate_click', ...})`.
- Include parameters: `affiliate_offer`, `affiliate_position`, `affiliate_page_id`, `affiliate_page_url`, `affiliate_cta_text`, `affiliate_tracking_version`, and `affiliate_url`.
- Browser-verify a click and capture the emitted event payload.
- State honestly that marking as GA4 key event and registering custom dimensions requires GA4 admin access if auth is missing.

GA4 admin tasks when access exists:
- Mark `affiliate_click` as a key event.
- Register custom dimensions for `affiliate_offer`, `affiliate_position`, `affiliate_page_id`, `affiliate_page_url`, `affiliate_cta_text`, `affiliate_tracking_version`.

## Homepage money-route block
Add a small, non-disruptive homepage block linking to main commercial hubs/review routes. Place it after the hero and before generic popular-topic browsing when possible so it does not break custom homepage headers or hero layout.

Verify homepage with browser/rendered view after placement; if it appears before the custom header/hero, reposition it inside the existing homepage flow.

## Final report requirements
Report:
- URLs passed/failed.
- Claims removed, grouped by URL.
- Sub-ID coverage totals and unsupported/opaque counts.
- GA4 status: site-side firing vs admin/UI completion.
- Homepage money-route status.
- Next 7-day KPI baseline plan focused on Affiliate CTR, EPC, RPM, and revenue per page.

## Pitfalls
- Do not confuse cache-busted success with full CDN purge. If no Cloudflare token is available, say purge was unavailable and rely on cache-busted public verification.
- Do not claim GA4 key-event/custom-dimension setup unless you actually used authenticated GA4 Admin/UI/API access.
- Do not add fake `Review` anchor links in tables unless real target anchors exist; use neutral text like `Current guide` or real review URLs.
- Regex cleanup can remove too much; back up raw post content before claim cleanup and verify visible content/word count after edits.