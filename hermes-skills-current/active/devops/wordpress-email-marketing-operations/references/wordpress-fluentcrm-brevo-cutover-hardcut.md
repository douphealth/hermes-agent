<!-- Consolidated from skill: wordpress-fluentcrm-brevo-cutover-hardcut; original path: /home/hermes/.hermes/skills/devops/wordpress-fluentcrm-brevo-cutover-hardcut -->

---
name: wordpress-fluentcrm-brevo-cutover-hardcut
description: Hard-cut a WordPress email signup flow from legacy FluentCRM/Brevo routes to a new branded delivery path when old welcome emails or reply-to headers keep leaking through.
---

# WordPress FluentCRM/Brevo Hard-Cut Cutover

Use this when a site appears partially fixed, but new signups still trigger an old welcome email, old sender, or old reply-to.

## Typical symptoms
- User receives the wrong welcome subject from a legacy flow.
- Sender/reply-to still shows an old address even after new snippets were deployed.
- Homepage form says `Try again` even though the email is delivered.
- Direct branded test route works, but homepage signup still fires the old path.

## Proven workflow

1. **Find every active email path, not just the newest snippet.**
   - Inspect Code Snippets for old subjects, old reply-to addresses, old sender addresses, and legacy endpoints.
   - Search for strings like:
     - old subject line
     - old reply-to Gmail
     - old branded address
     - `/wp-json/.../send-now`
     - `/wp-json/.../capture`

2. **Inspect FluentCRM automation layers too.**
   - List funnels, sequences, and campaigns.
   - Old FluentCRM funnels can still fire on `contact_created` even after a new custom route exists.
   - If they are part of the old path, set those funnels to `draft` before claiming the cutover is done.

3. **Do not trust a successful direct branded send as proof the homepage flow is fixed.**
   - A direct route can work while the homepage still calls the legacy route.
   - Verify the actual homepage script and signup endpoint wiring separately.

4. **Hard-cut the homepage flow away from the legacy custom routes.**
   - If the homepage uses old proxy endpoints like legacy `capture` / `send-now`, replace that logic entirely.
   - Prefer:
     - direct subscriber creation via `/wp-json/fluent-crm/v2/subscribers`
     - direct branded send via the new Brevo API helper
   - This is more reliable than chaining homepage signup through older intermediary endpoints.

5. **Handle empty 200 responses defensively.**
   - On some WordPress stacks with optimization/minification layers, a custom REST route can return HTTP `200` with an empty body.
   - Frontend JS must not assume `r.json()` will succeed.
   - Safer pattern:
     - `await r.text()`
     - try `JSON.parse(text)`
     - if HTTP status is OK and body is empty, still treat the request as success when that matches the backend contract.
   - Backend side: prefer returning `new WP_REST_Response(...)` explicitly.

6. **Verify the public homepage HTML, not just snippet storage.**
   - After updating snippets, fetch the live homepage HTML and confirm the old endpoints/addresses are gone.
   - Check for absence of:
     - old legacy route URLs
     - old Gmail reply-to address
     - old sender address
   - Check for presence of the new signup route only.

7. **Then run a real branded send proof.**
   - Hit the branded direct-test endpoint and capture the accepted message ID.
   - This confirms the new delivery layer is still live after the hard cut.

## High-value verification checklist
- Old FluentCRM funnels are `draft`.
- Homepage HTML no longer contains old `capture` / `send-now` routes.
- Homepage HTML no longer contains old reply-to/sender strings.
- New branded direct send returns `201`/accepted with a message ID.
- Frontend form no longer shows false failure for a successful request.

## Important lesson
A WordPress email cutover is not complete until **all three** are true:
1. old automations are disabled,
2. homepage HTML points only at the new path,
3. a real live signup no longer produces the legacy email headers.
