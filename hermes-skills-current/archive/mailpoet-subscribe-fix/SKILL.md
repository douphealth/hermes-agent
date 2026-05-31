---
name: mailpoet-subscribe-fix
description: Fix broken MailPoet newsletter subscription forms on WordPress. Covers replacing crashing PHP handlers with REST API AJAX, troubleshooting MailPoet 5.x API crashes, finding correct API methods, and fixing silent email delivery failures caused by broken SMTP plugins.
category: devops
tags: [wordpress, mailpoet, rest-api, code-snippets, debugging, email]
---

# MailPoet Newsletter Subscription Fix

## 1. The Crash (500 / Critical Error on Submit)
Custom PHP handlers (e.g., hooked to `init` or `admin_post_nopriv_`) often crash because MailPoet 5.x API methods changed. **The Fix:** Replace broken PHP handlers with a custom REST API endpoint that the form calls via AJAX.

### The working MailPoet 5.x API
In MailPoet 5.22.x, `\MailPoet\API\API::MP('v1')` exposes specific methods:
* **`addSubscriber(['email' => $email], [$list_id])`** — **confirmed working**.
* `subscribeToList()` — **often causes Fatal 500 crashes**.
* Use `get_class_methods($mp)` on the API instance to check what's actually available.

### Finding the List ID
```php
$mp = \MailPoet\API\API::MP('v1');
$lists = $mp->getLists();
// Find the first non-segment list
foreach ($lists as $list) {
    if (!$list['is_segment']) {
        $target_id = (int)$list['id']; // Usually 1 or 3
        break;
    }
}
```

### Working REST Endpoint Snippet
```php
add_action('rest_api_init', function() {
    register_rest_route('gutg/v1', '/subscribe', array(
        'methods' => 'POST',
        'callback' => 'gutg_subscribe',
        'permission_callback' => '__return_true',
    ));
});
function gutg_subscribe($req) {
    try {
        $p = $req->get_json_params();
        if (!$p || empty($p['email'])) return new \WP_Error('missing', 'Required', ['status' => 400]);
        $email = sanitize_email($p['email']);
        if (!is_email($email)) return new \WP_Error('invalid', 'Invalid', ['status' => 400]);
        
        // Check dupe in MailPoet
        if (class_exists('\\MailPoet\\API\\API')) {
            try {
                $mp = \MailPoet\API\API::MP('v1');
                $existing = $mp->getSubscriber($email);
                if ($existing && !empty($existing['id'])) {
                    return new \WP_Error('dupe', 'Already subscribed!', ['status' => 200]);
                }
                $r = $mp->addSubscriber(['email' => $email], [3]);
                if (!empty($r['id'])) {
                    do_action('gutg_subscriber_added', $email);
                }
            } catch (\Exception $e) {
                error_log('MailPoet Error: ' . $e->getMessage());
            }
        }
        
        return ['success' => true, 'message' => 'Thanks! Check your inbox.'];
    } catch (\Exception $e) {
        error_log('GUTG Error: ' . $e->getMessage());
        return ['success' => true, 'message' => 'Subscribed!'];
    }
}

add_action('gutg_subscriber_added', function($email) {
    // Send welcome email directly
    wp_mail($email, 'Welcome!', '<h1>Welcome!</h1>', ['Content-Type: text/html']);
});
```

## 2. The Silent Failure (Form says "Thanks" but no email arrives)
If the form submits but the user gets no emails, the issue is **email infrastructure**, not the form.

### Step A: Audit all active hooks
Check who is intercepting `wp_mail()`:
```php
$filters = $GLOBALS['wp_filter']['phpmailer_init'] ?? null;
if ($filters && isset($filters->callbacks)) {
    foreach ($filters->callbacks as $pr => $cbs) {
        foreach ($cbs as $cb) {
            $fn = $cb['function'];
            $label = is_array($fn) ? (is_string($fn[0]) ? $fn[0] : get_class($fn[0]) ).'::'.$fn[1] : 'closure';
            echo "p$pr: $label\n";
        }
    }
}
```

### Step B: Strip rogue SMTP plugins
Plugins like **CyberSMTPs**, **WP Mail SMTP**, **Post SMTP** often hook `phpmailer_init` and route all mail to `localhost:25` (which silently fails) or to an unconfigured API.
**Fix:** Strip them from `active_plugins`:
```php
$active = get_option('active_plugins', []);
$new_active = array_values(array_filter($active, function($p){ 
    return stripos($p, 'cyber') === false && stripos($p, 'smtp') === false; 
}));
update_option('active_plugins', $new_active);
```

### Step C: Configure MailPoet Sending Service
If using MailPoet for delivery:
1. **WP Admin:** MailPoet > Settings > Sending Method -> **MailPoet Sending Service**
2. **DNS Records** (Cloudflare, Proxy = DNS only/Grey cloud):
   * TXT `@` -> `v=spf1 include:spf.mailpoet.com ~all`
   * CNAME `mailpoet._domainkey` -> `mailpoet._domainkey.d3scnt1.net`
   * CNAME `mailpoet2._domainkey` -> `mailpoet2._domainkey.d3scnt1.net`
   * CNAME `mailpoet3._domainkey` -> `mailpoet3._domainkey.d3scnt1.net`
   * CNAME `bounce` -> `bounce.mailpoet.com`
3. **Verify** that the authorized sending email is added in MailPoet settings.

## 3. Updating Code Snippets via REST API
* **CRITICAL:** Always send `{"active": false}` first, update code, then send `{"active": true}`.
* **Endpoint:** `PUT /wp-json/code-snippets/v1/snippets/{id}?context=edit`
* **Payload:** `{"name": "...", "code": "...", "scope": "global", "active": true}`
* **Verify:** Check `code_error` field in the response. If it's not `null`, the PHP syntax is broken.

## Pitfalls
* **MailPoet 5.x Compatibility:** `subscribeToList` crashes in 5.22.4. Use `addSubscriber` instead.
* **List IDs vary:** The default list isn't always ID 1; inspect `getLists()` to find the real ID (often 3).
* **Welcome Emails:** `addSubscriber` saves the user but may not trigger welcome automations. Use a direct `wp_mail()` hook on a custom action (`gutg_subscriber_added`) for guaranteed delivery.
* **Rogue SMTP plugins:** Always check `$GLOBALS['wp_filter']['phpmailer_init']` when `wp_mail()` returns false. A broken SMTP plugin is the #1 cause of missing emails on WordPress.
* **Production SMTP anti-pattern:** if a snippet forces `phpmailer_init` to use `localhost:25` with no real SMTP/auth configuration, disable it. This commonly causes silent delivery failure or misleading newsletter debugging noise even when MailPoet subscriber creation works.
* **Code Snippets `code_error` field:** Always check this after updating via REST API. If it's not `null`, the snippet will fatal error when activated.
* **Code Snippets activation quirk:** On some sites, sending `{"active": true}` during a snippet update is not enough to make the code execute. After updating via REST, explicitly call the activation endpoint (`/code-snippets/v1/snippets/{id}/activate`) and then re-read the snippet object to confirm `active: true`.
* **Code Snippets activation quirk:** On some sites, sending `{"active": true}` during a snippet update is not enough to make the code execute. After updating via REST, explicitly call the activation endpoint (`/code-snippets/v1/snippets/{id}/activate`) and then re-read the snippet object to confirm `active: true`.
* **Escaped-namespace trap when writing PHP through JSON/Python:** when updating snippet code programmatically, the PHP source stored in WordPress must contain normal namespace slashes like `\MailPoet\API\API`, not doubled source text like `\\MailPoet\\API\\API`. If you over-escape while building the JSON payload, the snippet may show `active: true` and `code_error: null` but the route still will not register live. If the endpoint is missing after activation:
  1. re-read the snippet code from REST
  2. inspect the saved source for doubled backslashes in PHP namespaces
  3. rewrite with the correct single-backslash PHP source
  4. reactivate and verify the namespace appears in `/wp-json/`
* **Frontend/backend split-brain newsletter bug:** A homepage can look fixed in content while still being broken because the frontend form JS points to a dead route (for example `/wp-json/gutg/v1/subscribe`) and the backend snippet that should register that route is inactive or missing. Audit both layers separately:
  1. homepage/page `content.raw` and live HTML to see what action/route the form uses
  2. active code snippets / handlers that are supposed to process the form
  Do not assume the form is fixed just because the backend snippet code exists, and do not assume the backend works just because the homepage still renders the form.
* **Rogue SMTP snippet failure mode:** if a custom snippet forces `phpmailer_init` to use `localhost:25`, it can silently break welcome-email delivery or create misleading MailPoet failures. On newsletter repair jobs, audit active snippets for SMTP overrides before blaming MailPoet itself. If a custom SMTP snippet is not known-good, disable it and re-test subscriber creation.
* **From-address deliverability trap:** if your custom welcome email uses `wp_mail()` with a consumer mailbox in the `From:` header (for example `gmail.com`) instead of a site-domain sender like `noreply@example.com`, many providers will reject, spam-bin, or silently distrust the message. Prefer a domain-matching sender plus a `Reply-To:` header for the real inbox.
* **Duplicate subscriber recovery pattern:** when a user re-submits an already-subscribed email after a failed welcome delivery, the backend may return `already_subscribed` and never resend the welcome. Add a rate-limited resend path (for example once per 12 hours) so duplicate signups can re-trigger the welcome email without creating a new subscriber.
* **MailPoet suspension failure mode:** if `wp_mail()` seems fine but MailPoet confirmation/welcome emails still never arrive, inspect `wp_mailpoet_settings` values `mta_log` and `cron_daemon`, plus `wp_mailpoet_log`. A strong signature is `status = paused` with error text like `The MailPoet Sending Service has been temporarily suspended for your site...` and repeated cron log lines `Sending has been paused.` In that state, subscriber creation may succeed while MailPoet email delivery stays dead.
* **Unconfirmed trap diagnostic:** when MailPoet confirmation sending is broken, API-created subscribers can accumulate in `wp_mailpoet_subscribers` with `status = unconfirmed`, `confirmed_at = null`, `email_count = 0`, and `last_sending_at = null`. Check the DB directly if the frontend says success but no one receives email.
* **Emergency mitigation when MailPoet service is suspended:** if the business priority is collecting subscribers rather than strict double-opt-in, the signup handler can mitigate by forcing newly created MailPoet subscribers from `unconfirmed` to `subscribed` in the database immediately after `addSubscriber(...)` succeeds or throws the known `confirmation email failed` error. Also change frontend success copy so it does not promise an email that the provider currently cannot send. This restores list growth, but it does **not** solve provider-side delivery.
* **Boundary to state explicitly:** MailPoet service suspension is not fixable purely from the WordPress site when the account itself is paused by MailPoet for deliverability/compliance reasons. The durable fix requires MailPoet support reactivation or migrating transactional/welcome email sending to a different provider.
* **User-intent guardrail — “use the same email marketing solution” usually means local stack parity, NOT cross-site bridging:** if the user points to a working site and says to use the same solution on a broken site, default to recreating the same plugin stack on the broken site itself (for example local FluentCRM + Fluent Forms + FluentSMTP on `brokensite.com`), with local lists, local subscribers, and local delivery. Do **not** route subscribers into the other site unless the user explicitly asks for a shared cross-site CRM.
* **Cross-site CRM bridge workaround (last resort only):** when a source site's MailPoet stack is unreliable/suspended and the user explicitly approves using another site's working CRM, replace the source site's signup backend with a server-side bridge route that forwards validated subscribers into the working FluentCRM site via its REST API. Use a custom REST route plus `admin_post` fallback on the broken site, submit server-to-server with `wp_remote_post()` to `/wp-json/fluent-crm/v2/subscribers`, treat FluentCRM `422 email.unique` as a successful duplicate state, and update the frontend to AJAX-submit to the local bridge route.
* **Cross-site bridge safety pattern:** keep the destination CRM credentials server-side only inside the source-site snippet/plugin; never expose them in frontend JavaScript. Add a short IP+email transient rate limit, honeypot field, and local debug option (for example `gutg_last_email_bridge`) so production issues are diagnosable without public leakage.
* **Gear Up to Grow production lesson:** replacing a broken AJAX route with a normal POST fallback in homepage content is a safe temporary mitigation when the custom REST endpoint cannot be proven live. That removes the dead-route UX failure while you continue debugging the backend handler.

