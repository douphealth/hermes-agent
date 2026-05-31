<!-- Consolidated from skill: wordpress-brevo-sequence-hardcut; original path: /home/hermes/.hermes/skills/devops/wordpress-brevo-sequence-hardcut -->

---
name: wordpress-brevo-sequence-hardcut
description: Hard-cut broken WordPress email signup/sequence systems onto direct Brevo delivery, disable legacy automations, and verify branded reply-paths end-to-end.
category: devops
tags: [wordpress, brevo, email, fluentcrm, code-snippets, rest-api, cloudflare]
---

# WordPress Brevo Sequence Hard-Cut

Use this when a WordPress site has a messy email stack: old FluentCRM automations, broken SMTP, mixed wp_mail behavior, confusing homepage signup flows, or wrong From/Reply-To identities still leaking through after partial fixes.

## When to use
- Signup form says failure but email still arrives
- Wrong From / Reply-To keeps appearing after a supposed fix
- SMTP auth is flaky or broken
- FluentCRM/legacy automations are still firing old welcome emails
- You need a fast, production-safe hard cut to a branded Brevo path

## Core pattern
1. **Back up active snippets/funnels first** to `/tmp/...`.
2. **Discover all active send paths** before editing:
   - Code Snippets REST API
   - custom REST routes in `/wp-json/`
   - FluentCRM funnels/automations
   - FluentSMTP / SMTP debug routes if present
3. **Do not trust the latest snippet alone.** Old emails often come from:
   - legacy FluentCRM `contact_created` funnels
   - older custom REST routes like `/send-now`
   - `wp_mail()` interception layers
4. **Move the real delivery path to Brevo**:
   - Preferred: direct `https://api.brevo.com/v3/smtp/email`
   - Acceptable fallback: `wp_mail()` only if a known Brevo pre-filter/interceptor is already installed and verified
5. **Use branded sender + branded replyTo** in the payload.
6. **Hard-cut homepage signup flows** so the frontend no longer calls the old route.
7. **Disable obsolete funnels** by setting them to draft if they are hijacking new subscribers.
8. **Verify with live sends and debug state**, not assumptions.
9. **If the site has no workable email plugin stack, install/activate Code Snippets and deploy the mail system as new snippets instead of trying to force plugin-native automations.** This is often faster and more reliable than fighting CF7/UAGB/Elementor form handlers or half-configured CRM plugins.

## Recommended architecture
### Best
- custom signup REST route
- direct subscriber create/update (FluentCRM if needed)
- direct Brevo API send for welcome / sequence messages
- branded sender address
- branded replyTo address

### Avoid
- mixing broken SMTP with new API sends
- leaving old `send-now` or legacy autoresponder routes active
- assuming `wp_mail()` is safe unless you explicitly verified where it goes

## Practical workflow
### 1) Inventory the live system
Check:
- `/wp-json/` namespaces and routes
- `/wp-json/code-snippets/v1/snippets`
- `/wp-json/fluent-crm/v2/funnels`
- any custom debug/status routes

Look specifically for:
- `send-now`
- `capture`
- `subscribe`
- `smtp-debug`
- `direct-branded-test`
- old Gmail reply addresses
- old sender identities

### 2) Inspect current snippet code
Search for:
- `wp_mail(`
- `api.brevo.com/v3/smtp/email`
- `Reply-To:`
- `replyTo`
- old mailbox addresses
- old subject lines that still appear in received emails

### 3) Test the real legacy path
If the site still sends the wrong email, trigger the actual public signup flow and compare against the code you think is active.

Important lesson:
- the **received email headers** are stronger evidence than your assumptions about which route is active

### 4) Disable legacy FluentCRM automations if needed
If old welcome emails still fire:
- back up funnels first
- set obsolete funnels to `draft`
- re-test with a fresh signup

This is often the real fix when the code looks correct but the mailbox proves otherwise.

### 5) Replace public signup route with a hard-cut route
Recommended pattern:
- validate email
- create/update subscriber directly
- send premium welcome email through direct Brevo helper
- return a real `WP_REST_Response(..., 200)`

## Frontend lesson: empty 200 body bug
Some custom REST signup endpoints can return **HTTP 200 with an empty body** even when the action succeeded.

If frontend JS does `return r.json()` blindly, it throws and shows a false error like `Try again.`

Safer frontend pattern:
```js
fetch('/wp-json/...', {...})
  .then(async (r) => {
    const t = await r.text();
    let d = {};
    try { d = t ? JSON.parse(t) : {}; } catch (_) { d = {}; }
    if (!r.ok) throw new Error((d && d.message) || 'Request failed');
    return d;
  })
```
Treat `r.ok` + empty body as success when the server-side action is known to be side-effectful and verified.

## Brevo direct-send helper pattern
Use a helper that:
- validates recipient
- posts to Brevo API
- stores last status / messageId / error in an option for verification

Payload essentials:
```php
array(
  'sender' => array('name' => 'Brand', 'email' => 'hello@example.com'),
  'replyTo' => array('name' => 'Brand', 'email' => 'hello@example.com'),
  'to' => array(array('email' => $to)),
  'subject' => $subject,
  'htmlContent' => $html
)
```

## Verification checklist
Do all of these:
1. Trigger a real public signup
2. Trigger a direct branded test route if available
3. Check latest debug option / last delivery log
4. Confirm the received email headers show the correct:
   - From
   - Reply-To
   - subject
5. Confirm old routes are gone from public HTML if you hard-cut them
6. Confirm obsolete funnels are draft if they were part of the problem

## Critical findings to remember
- A successful code update does **not** mean the public signup flow is using that code path
- A legacy FluentCRM funnel can silently override your new branded path
- Public homepage HTML is worth checking directly to ensure old JS endpoints are really gone
- Plantastic-style setups may use `wp_mail()` safely only because `pre_wp_mail` is intercepting to Brevo; verify interception explicitly before trusting it
- If SMTP auth is broken, stop trying to salvage it unless there is a strong reason; direct Brevo API is cleaner and more deterministic
- Some sites have **no useful CRM stack at all** but do expose plugin installation via `/wp-json/wp/v2/plugins`. In that case, installing and activating `code-snippets/code-snippets`, then deploying a direct Brevo route + signup UI via snippets, is a reusable production shortcut.
- When homepage or lead-magnet pages already contain visible forms from CF7, Elementor, or UAGB/Spectra, do not assume the plugin form should remain the source of truth. Two reliable rescue patterns emerged:
  1. **replace the form block entirely** with a direct HTML form that POSTs to your custom REST route; or
  2. **hard-cut the visible form in the browser** with footer JS that intercepts submit in the capture phase and posts to the new route instead.
- Prefer full replacement when the original block is easy to swap by REST and the site is cache-stable. Prefer JS hard-cut when the visible form is already embedded deep inside a builder layout and you need a fast production-safe override.
- Verification standard for this pattern is three-layered:
  1. route/debug proof (`/wp-json/<ns>/debug` shows subscriber + `last_mail` with Brevo `201`),
  2. browser proof (visible form shows success state),
  3. provider proof (Brevo events show `delivered` / `opened`, not just `requests`).

### Dedicated Brevo account lessons
When the user requires **one Brevo account per site** plus **own-domain sender identity**, do not treat "Brevo-backed" as sufficient. Verify isolation explicitly.

### What to verify per site
1. The snippet/API key is unique to that site's Brevo account
2. The sender email belongs to that site's domain
3. The reply-to also matches the intended site identity
4. The Brevo account is actually activated for transactional sending
5. The domain authentication state is ready, not just the sender object

### Critical Brevo findings
- `POST /v3/senders` can succeed and create an own-domain sender even when the account is not truly production-ready.
- `POST /v3/senders/domains` can also succeed and return DNS instructions, while the account still cannot send transactional mail.
- High-value failure signature when the dedicated account exists but is not activated:
  - `403 permission_denied`
  - `Unable to send email. Your SMTP account is not yet activated. Please contact us at contact@brevo.com to request activation`
- Helpful probe:
  - `GET /v3/account`
  - if `relay.enabled` is `false`, treat transactional sending as blocked until proven otherwise.
- Stronger production finding: even after `GET /v3/senders/domains/<domain>` shows `verified:true` and `authenticated:true`, Brevo can still block transactional sends if `relay.enabled` remains `false`. That means DNS/domain auth is complete but account-level transactional approval is still missing.
- `GET /v3/senders/domains` may show the domain present but still `authenticated:false` / `verified:false`; do not switch production delivery to that account until either sending is proven or the user accepts temporary risk.
- Useful endpoint detail: `PUT /v3/senders/domains/<domain>/authenticate` is the working auth call once DNS records are in place. Treat a successful authenticate response as only one checkpoint, not final proof that the account can send.
- New production lesson from Mice Gone Guide / EfficientGPTPrompts remediation:
  - a WordPress route can report local success (`200`, debug says `last_mail.status:201`, messageId present) while Brevo later emits an `error` event for the same message because the chosen sender identity is invalid on that specific Brevo account.
  - high-value failure signature on the shared/live account:
    - `Sending has been rejected because the sender you used <address> is not valid. Validate your sender or authenticate your domain`
  - do **not** assume a sender is usable just because the domain is authenticated elsewhere or because a sender object can be created in Brevo.
  - after creating a sender on the shared/live Brevo account, re-read `/v3/senders` and inspect whether the new sender is actually `active:true`. A newly created sender can exist but still be `active:false`, and mail using it may fail.
  - if production delivery is broken and the dedicated/site-specific Brevo account still has `relay.enabled:false`, the fastest safe rescue is:
    1. keep the live site on the already-working shared Brevo account,
    2. create an override snippet with higher priority than the old route/snippet,
    3. force the sender to a known validated active sender on that shared account,
    4. keep site branding in the sender name / email copy / CTA structure,
    5. set `replyTo` to the centralized mailbox the user wants,
    6. verify with a fresh signup plus Brevo event logs until you see `delivered`, not just `requests`.
  - strong verification standard for these rescues:
    1. route returns success,
    2. site debug/state shows the subscriber + step state updated,
    3. Brevo events show `delivered` for a fresh recipient,
    4. if events show `error`, trust the provider event stream over local site debug.
- New production lesson from cross-domain sender fallout:
  - if the user requires **the email to be sent by the corresponding domain**, a generic fallback sender from another site is not an acceptable final state even if it restores delivery.
  - before hard-cutting to a fallback sender, test whether the shared/live Brevo account can legally send from the target domain after authenticating that domain on the shared account.
  - reusable sequence for shared-account own-domain rescue:
    1. add/fix the target domain in the shared/live Brevo account,
    2. fetch exact DNS records from `GET /v3/senders/domains/<domain>`,
    3. update DNS with the exact Brevo code + DKIM + DMARC values,
    4. call `PUT /v3/senders/domains/<domain>/authenticate`,
    5. create or re-check the target sender with `POST /v3/senders` and `GET /v3/senders`,
    6. send a direct provider probe and inspect Brevo events until you see `delivered` from the target domain sender.
- Multiple `brevo-code:` TXT records at the apex can block or confuse Brevo domain auth. The exact Brevo code must match the account being authenticated. If old codes from another Brevo account remain in DNS, remove them once the correct account is authenticated.
- A shared/live Brevo account can sometimes send from a site's own domain even when that site's dedicated Brevo account is suspended or has `relay.enabled:false`. Treat the provider event stream as the source of truth.
- Dedicated-account support/contact requests can reveal a harsher blocker than simple SMTP inactivity: the entire account may be placed into Brevo compliance review / suspension. Failure signature from UI: account suspended / additional verification required / terms-of-use violation. In that state, do not keep retrying sends; use support-review language instead.
- When asking the user to contact Brevo, distinguish clearly between these two states:
  1. **SMTP not activated** (`relay.enabled:false`, 403 permission_denied), and
  2. **Account suspended / under compliance review** (deliverability center says suspended).
  4. call `PUT /v3/senders/domains/<domain>/authenticate`,
  5. re-read the domain object until `verified:true` and `authenticated:true`,
  6. create/re-read the sender object,
  7. send a real probe mail and verify provider events.
- high-value nuance: Brevo event visibility can lag. A `201` API response plus an empty immediate event query is **not** enough to call success or failure. Poll the event endpoint for several seconds before concluding.
- stronger rescue order when the user requires "each site sends from its own domain":
      1. try to authenticate that site's domain on the shared/live Brevo account,
      2. test whether the shared account can deliver using the site-domain sender,
      3. only use a foreign fallback sender if the provider still rejects the site-domain sender,
      4. if you must use a foreign fallback temporarily, label it as temporary and correct it as soon as the domain sender becomes valid.
- new recovery lesson from Mice Gone Guide dedicated-account reactivation:
      - if Brevo support later activates the dedicated account's transactional SMTP / relay, do not leave the site on the temporary shared-account fallback.
      - immediate cutback sequence:
        1. verify `GET /v3/account` now shows `relay.enabled:true`,
        2. verify the dedicated domain object shows `verified:true` and `authenticated:true`,
        3. send a direct provider probe from the dedicated sender and confirm provider events,
        4. patch the live WordPress override snippet to use the dedicated API key + dedicated domain sender,
        5. keep or deactivate staged snippets so there is only one clear live send path,
        6. remove stale apex `brevo-code:` TXT records from older/shared accounts so only the correct code remains,
        7. re-test through the real public signup route and confirm `delivered` from the dedicated sender.
      - source of truth remains the provider event stream: the final proof is `delivered` with the correct domain sender, not just local `201` debug.
- if production delivery is broken and the dedicated/site-specific Brevo account still has `relay.enabled:false`, the fastest safe rescue is:
    1. keep the live site on the already-working shared Brevo account,
    2. create an override snippet with higher priority than the old route/snippet,
    3. first test whether the shared account can send with the site's own-domain sender (not every authenticated sender is exposed as `active:true`, and the API `201` is not enough),
    4. if provider events show `delivered`, switch the live route to the site-domain sender immediately,
    5. if provider events show `error`, fall back to the known validated shared sender,
    6. keep site branding in the sender name / email copy / CTA structure,
    7. set `replyTo` to the centralized mailbox the user wants,
    8. verify with a fresh signup plus Brevo event logs until you see `delivered`, not just `requests`.
  - new high-value DNS/auth lesson from Mice Gone Guide / FrenchyFab / MysticalDigits / EfficientGPTPrompts / GearUpToFit:
    - a domain can look mostly configured while Brevo still refuses authentication because the root TXT `brevo-code` value belongs to a different Brevo account.
    - strong failure signature in Brevo domain UI / API:
      - DKIM and DMARC are green
      - but `brevo_code.status:false`
      - authenticate call returns `bad_request`
      - message says the Brevo code in Brevo and in DNS mismatch.
    - do not just keep overwriting one TXT blindly. Check for **multiple `brevo-code:` TXT records** at the zone apex; an old leftover Brevo code from another account can coexist with the new one and create split-brain auth.
    - fix pattern:
      1. fetch the exact required DNS values from `GET /v3/senders/domains/<domain>` for the specific Brevo account,
      2. update/create the DKIM CNAMEs and DMARC TXT in DNS,
      3. ensure the apex TXT contains the **matching Brevo code for that account**,
      4. remove stale/older `brevo-code:` TXT records so only the correct one remains,
      5. then run `PUT /v3/senders/domains/<domain>/authenticate` again.
    - Cloudflare automation note: if you have a valid token with `#dns_records:edit`, you can repair these records directly by API and then verify publicly with DNS-over-HTTPS before retrying Brevo auth.
  - new provider-behavior lesson:
    - `POST /v3/smtp/email` returning `201` is still only request acceptance. Always confirm the follow-up event stream.
    - Some own-domain senders on the shared account can deliver even when the sender list still shows `active:false`; the event stream is the source of truth.
    - Therefore use this decision rule:
      - `requests + delivered` => sender is usable in production
      - `requests + error` => sender is not yet usable, regardless of UI optimism.
  - strong verification standard for these rescues:
    1. route returns success,
    2. site debug/state shows the subscriber + step state updated,
    3. Brevo events show `delivered` for a fresh recipient,
    4. if events show `error`, trust the provider event stream over local site debug.


    - some sites are not just suffering from a bad signup route; they also have legacy `wp_mail()` traffic still escaping through old FluentSMTP / SMTP plugin paths.
    - if you prove the custom signup route works but SMTP-backed test sends or older automations remain unreliable, add a **high-priority transport override snippet** that intercepts `wp_mail` with `pre_wp_mail` and forwards mail through the already-working Brevo fallback account.
    - tag these rescue sends distinctly (for example `smtp-rescue`) and store a debug option like `*_last_wp_mail_rescue` so you can verify exactly what the interception layer sent.
    - then expose a small authenticated REST probe route (for example `/smtp-rescue-test`) that triggers `wp_mail()` intentionally. This lets you verify the legacy SMTP layer is truly bypassed.
    - production-safe sequence for mixed stacks:
      1. hard-cut the visible/public subscribe route to the working Brevo fallback sender,
      2. if legacy mail still exists elsewhere, add `pre_wp_mail` interception at very high priority,
      3. verify both the signup path and the `wp_mail` rescue path with fresh provider events,
      4. only then consider the site's SMTP problem actually contained.
  - new dedicated-account lesson from Mystical Digits:
    - a dedicated Brevo account can show `relay.enabled:true` and still not be ready for branded production sending if the own-domain sender is `active:false` or the domain object is still `authenticated:false` / `verified:false`.
    - in that situation, do not trust the dedicated sender path just because the account itself has SMTP enabled.
    - if the site is already live on a working fallback sender, create a higher-priority override snippet and move production traffic to the fallback path immediately, then leave the dedicated path for later remediation.

### Operational rule
If the user demands account isolation and sender/domain purity, prefer this order:
1. confirm dedicated API key
2. confirm dedicated sender object exists
3. authenticate the sender domain and verify DNS records publicly
4. confirm transactional sending works from that account with a real send test
5. only then patch the live site to use the dedicated account

If step 4 fails, do **not** claim the site is fully corrected. Report the external Brevo blocker explicitly.

### Safe staging pattern
When all WordPress-side code is ready but Brevo still blocks sending:
- create the dedicated-account override snippet anyway
- keep it **inactive** / staged
- name it clearly (for example `... Dedicated Brevo Override STAGED`)
- only activate it after a direct provider send succeeds from that Brevo account

This preserves production delivery while making final cutover instant once Brevo flips the account state.

### Post-approval cutover pattern
When Brevo support later activates the dedicated account, do **not** just assume the site is fixed. Use this exact cutover sequence:
1. verify `GET /v3/account` now shows `relay.enabled:true` on the dedicated account
2. verify the dedicated domain object still shows `verified:true` and `authenticated:true`
3. send a direct provider probe from the dedicated account using the real site-domain sender and inspect provider events until you see `delivered`
4. update the live WordPress snippet/route so it uses the dedicated API key and the site-domain sender
5. keep the live override at the highest priority; do not reactivate older lower-priority rescue snippets accidentally
6. run a fresh public signup and verify:
   - route/debug success on the site
   - provider event `delivered`
   - `from` matches the site's own domain sender
7. remove stale DNS leftovers that belonged to older Brevo accounts, especially old apex `brevo-code:` TXT records, once the correct account is authenticated

High-value lesson from Mice Gone Guide:
- the support approval flips the real blocker (`relay.enabled:true`), but you still must actively cut the site back from the temporary fallback path to the dedicated sender path.
- after cutover, the verification standard is not just `201` from the API; it is a fresh public signup plus a provider event showing `delivered` from the site's own sender.

### Last-resort access pattern
If API-level work is exhausted and the blocker appears to be a Brevo web-account activation/review step:
- attempt Brevo web login only if you actually have the correct mailbox credentials
- if login creds are unavailable, trigger the Brevo password-reset flow for the relevant account mailbox so the user can reset and send you updated credentials
- do not promise web-UI completion unless you can actually authenticate into the mailbox-backed Brevo account

### Operational rule
If the user demands account isolation and sender/domain purity, prefer this order:
1. confirm dedicated API key
2. confirm dedicated sender object exists
3. confirm transactional sending works from that account with a real send test
4. only then patch the live site to use the dedicated account

If step 3 fails, do **not** claim the site is fully corrected. Report the external Brevo blocker explicitly.

## Good final outcome
A site is truly fixed only when:
- public signup works
- user-facing form feedback is correct
- delivered email uses the intended branded From / Reply-To
- old legacy routes/funnels are no longer the source of mail
- live provider acceptance is verified with a real message ID
- if the user requested dedicated-account isolation, the site is using its own Brevo key/account and not a borrowed sender path
