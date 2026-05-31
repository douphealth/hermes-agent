# Monetized App Funnel QA Reference

Use this when dogfooding freemium tools/apps whose business model depends on lead capture, saved results, checkout, affiliate offers, or premium unlocks.

## Core funnel to verify

`SEO landing page → freemium app/quiz → email capture/result save → personalized recommendation/result → paid upgrade or affiliate offer → automated nurture`

## Evidence checklist

- Entry path: confirm the SEO/blog/landing page links to the correct app URL with any expected UTM parameters.
- Freemium path: complete the quiz/tool with realistic inputs; verify a free result is produced without requiring payment.
- Backend personalization: do not accept a pretty frontend as proof. Check console/network/static JS for failed AI/result-generation calls or template fallback messages.
- Email capture: submit a QA email and verify whether the app only stores email in `localStorage` or actually confirms server-side lead persistence/email delivery before unlocking results.
- Result save: look for server-side lead/result save calls, captured quiz answers, UTM/source fields, segment assignment, and success/failure handling.
- Premium/paid path: click the paid CTA far enough to verify checkout creation or affiliate redirect. A locked-module UI alone does not prove monetization works.
- Offer matching: verify recommendations/upsells are based on quiz segment/problem/urgency rather than generic static cards.
- Tracking: verify events for `quiz_started`, `quiz_completed`, `email_submitted`, `lead_saved`, `free_result_viewed`, `premium_cta_clicked`, `checkout_created`, and `purchase_completed` where applicable.

## Useful techniques

1. Use `browser_console(clear=true)` before testing, then inspect console after each major step. Console logs such as `using template fallback`, `FunctionsFetchError`, or `Checkout error` are high-value monetization bugs.
2. Use `browser_snapshot()` to capture visible free result sections, locked premium modules, and CTA labels/prices.
3. Use `browser_vision()` for visual gating quality: whether results are blurred/teased, whether email capture is prominent, and whether the paid offer is persuasive.
4. Inspect deployed JS bundles with `requests`/regex when the browser hides implementation details. Search for terms like `functions.invoke`, `create-payment`, `send-welcome-email`, `generate-plan`, `checkout`, `stripe`, `email`, `localStorage`, and provider hostnames.
5. Directly probe discovered backend endpoints where safe using public frontend keys/anon keys. Redact keys in outputs. DNS/host failures for backend providers can explain browser-side checkout and personalization failures.

## Common findings and severity

- Critical: paid checkout CTA fails to create checkout/redirect.
- Critical: backend provider hostname does not resolve or edge functions are unreachable.
- High: email gate unlocks results even when lead save/email send fails.
- High: AI/personalization function fails and silently falls back to generic templates.
- Medium: premium modules exist visually but no backend entitlement, delivery, or fulfillment evidence.
- Medium: recommendations are generic and not mapped to quiz segment.
- Medium: missing conversion events across funnel steps.

## Reporting format

For each app, report:

- Funnel shape: present/missing.
- Freemium: pass/partial/fail.
- Email capture/result save: pass/partial/fail.
- Personalized recommendation: pass/partial/fail.
- Premium/paid path: pass/partial/fail.
- Critical blockers: exact symptoms and evidence.
- Next fix: one prioritized action before auditing/scaling the rest.
