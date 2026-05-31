# Static App Funnel Resilience via WordPress REST

Use when a static/Lovable/GitHub Pages app has a good frontend funnel but revenue infrastructure fails because a client-side backend provider (Supabase Edge Functions, Stripe checkout function, email function, etc.) is unreachable.

## Production pattern learned from FrenchyFab Care Compass

Problem signature:
- App frontend loads and quiz/result/paid CTA exist.
- Browser console shows provider failures such as `FunctionsFetchError: Failed to send a request to the Edge Function`.
- AI/personalization falls back to a template or checkout button dead-ends.
- WordPress site/domain is available and REST credentials exist, but the app itself is static/deployed on GitHub Pages or similar.

Safe SOTA rescue:
1. **Do not fake payments.** Keep the original checkout path as the primary attempt if it exists.
2. Add WordPress REST fallback endpoints under the brand's own WP domain, for example:
   - `POST /wp-json/<brand-app>/v1/lead`
   - `POST /wp-json/<brand-app>/v1/checkout-intent`
3. Implement the endpoints with a small active Code Snippets snippet or plugin code:
   - CORS allowlist only the app domains and the main WP domain.
   - Accept JSON and sanitize `email`, `answers`, `utm`, `page_url`, and `user_agent`.
   - Persist records server-side as private posts/custom post type/options/transients, or at minimum a private audit post.
   - Send an admin notification via `wp_mail` if full CRM/email automation is not yet available.
   - Return compact JSON like `{ success: true, id: 123 }`; remember some WP responses may include a BOM, so clients should strip/parse defensively.
4. Update the static app with a thin backend adapter:
   - AI generation is progressive enhancement; deterministic/local result generation must still complete the user journey.
   - Email capture first stores locally, then calls the WP lead endpoint, then optionally tries the original provider email function.
   - Premium CTA first tries real checkout, then records a `checkout-intent` fallback if checkout creation fails.
   - User-facing fallback copy should be honest: e.g. “Checkout is being refreshed. We saved your priority access request.”
5. Deploy the app without disturbing the main site:
   - If `gh` is unavailable but a GitHub PAT is available from the approved secret file, use GitHub REST contents API to update source files and, if needed, upload the built `dist/` to `gh-pages`.
   - Build locally first; run tests if present.
   - If the app is served through Cloudflare, purge only the affected hostname/zone when possible.
6. Verify end-to-end:
   - REST route appears under `/wp-json/`.
   - OPTIONS preflight from the app origin returns correct CORS headers.
   - POST lead returns `200` with `success:true` and a persisted id.
   - POST checkout-intent returns `200` with `success:true`.
   - Live app HTML references the new deployed chunks; if the main bundle lazy-loads route chunks, inspect both the main JS and lazy chunk for the new endpoint string.
   - Browser QA through the visible app confirms email submit and premium CTA no longer dead-end.

## Funnel flow + internal-link repair lesson

When fixing a static-app monetization funnel that starts from a WordPress property, verify the user’s real path, not only backend endpoints. A clean funnel should distinguish these steps in copy and linking:

1. Main WP site or article cluster → SEO landing page or app CTA.
2. Free app CTA, e.g. “Get My Free Plan,” starts the quiz/app.
3. Email gate copy says “save/reveal the free personalized plan,” not “unlock,” so users do not confuse the free email step with the paid product.
4. Paid upsell copy stays explicitly paid, e.g. “Unlock My Care Vault — $7.99.”
5. Contextual internal links point both ways: the landing/app should link out to supporting topical content, and relevant existing WordPress posts should link in to the landing/app with natural anchors.

Fast REST pattern for orphaned app/landing pages:
- Search existing `posts`/`pages` via REST for semantically relevant terms.
- Skip sources that already contain the target URL.
- Back up each source object JSON.
- Insert a compact `<!-- wp:html -->` contextual CTA block near the end/conclusion; avoid generic sitewide link dumps.
- Purge Cloudflare and verify public source URLs contain both the landing-page URL and app URL when appropriate.

## Pitfalls

- Do not label an email capture as “Unlock” if a paid “Unlock” CTA exists later in the same flow; this creates payment-step confusion and weakens trust.
- A fallback lead/intent endpoint is not a real revenue fix by itself. Report it as a conversion-preserving safety net until Stripe/checkout is restored.
- GitHub Pages + Cloudflare can serve stale `index.html` while individual new chunk assets are already reachable. Verify the asset graph, not only the root HTML.
- Browser automation snapshots can show stale accessibility content even when the actual screenshot is blank after navigation; cross-check `document.documentElement.outerHTML`, console errors, and raw HTTP.
- When deploying GitHub Pages manually, update both source branch and `gh-pages` branch if the hosting setup serves built files from `gh-pages` rather than building from source.
- Avoid exposing Supabase anon keys, GitHub PATs, Stripe secrets, WP app passwords, or Cloudflare tokens in logs or replies; redact all secret values.
