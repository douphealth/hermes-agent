<!-- Consolidated from skill: wp-email-audit; original path: /home/hermes/.hermes/skills/wp-email-audit -->

---
name: wp-email-audit
description: Audit WordPress email marketing infrastructure using REST API when wp-admin is Cloudflare-blocked. Covers FluentCRM, FluentSMTP, FluentForms, Kadence ESP integrations, and form connectivity analysis.
category: mlops
tags: [wordpress, email, fluentcrm, audit, rest-api, seo]
---

# WordPress Email Marketing Audit & Remediation

## When to Use
- User reports emails not sending, forms not collecting, or wants email infrastructure audit
- Cloudflare blocks wp-admin access (wp-login returns 403)
- Need to audit FluentCRM, FluentSMTP, FluentForms, or Kadence ESP integrations

## Authentication
```python
import base64
# REST API credentials (Application Password) work even when Cloudflare blocks wp-login
rest_b64 = base64.b64encode(f"username:app_password".encode()).decode()
site = "https://example.com"
```

## Phase 1: Site Settings Discovery
```bash
# Get all settings including integration keys
curl -sS "https://example.com/wp-json/wp/v2/settings" \
  -H "Authorization=[REDACTED] $B64" -H "User-Agent: Mozilla/5.0"
```

Key Kadence integration keys to check:
- `kadence_blocks_mailerlite_api`
- `kadence_blocks_convertkit_api`
- `kadence_blocks_activecampaign_api_key`
- `kadence_blocks_activecampaign_api_base`
- `kadence_blocks_send_in_blue_api`
- `kadence_blocks_mail_chimp_api`
- `kadence_blocks_getresponse_api_key`
- `kadence_blocks_wire_subscribe`

## Phase 2: FluentCRM Audit
```bash
# Lists and subscribers
curl -sS "$site/wp-json/fluent-crm/v2/lists" \
  -H "Authorization=[REDACTED] $B64" -H "User-Agent: Mozilla/5.0"

# Tags
curl -sS "$site/wp-json/fluent-crm/v2/tags" \
  -H "Authorization=[REDACTED] $B64" -H "User-Agent: Mozilla/5.0"

# Funnels (automations)
curl -sS "$site/wp-json/fluent-crm/v2/funnels" \
  -H "Authorization=[REDACTED] $B64" -H "User-Agent: Mozilla/5.0"

# Sequences (email content)
curl -sS "$site/wp-json/fluent-crm/v2/sequences" \
  -H "Authorization=[REDACTED] $B64" -H "User-Agent: Mozilla/5.0"

# Campaigns
curl -sS "$site/wp-json/fluent-crm/v2/campaigns" \
  -H "Authorization=[REDACTED] $B64" -H "User-Agent: Mozilla/5.0"

# Integrations (SMTP/ESP connections)
curl -sS "$site/wp-json/fluent-crm/v2/setting/integrations" \
  -H "Authorization=[REDACTED] $B64" -H "User-Agent: Mozilla/5.0"

# Subscribers
curl -sS "$site/wp-json/fluent-crm/v2/subscribers" \
  -H "Authorization=[REDACTED] $B64" -H "User-Agent: Mozilla/5.0"
```

## Phase 3: Form Audit
```bash
# Fetch live homepage HTML
curl -sS "$site/" -o /tmp/check.html

# Check forms: look for action="#" (dead), action="http" (external), or no form at all
# Look for exit-intent scripts, JavaScript handlers for form submit
```

If the remediation includes rewriting on-page email capture copy, trust panels, or inline HTML modules around forms, also load `wordpress-sota-seo-content-system` so the content looks premium and human instead of like generic marketing sludge.

## Phase 4: Frontend Form Testing
```bash
# Test FluentCRM public opt-in via admin-ajax
curl -sS -X POST "$site/wp-admin/admin-ajax.php" \
  -d "action=fluent_crm_api_optin&email=test@test.com&first_name=Test&list_ids%5B%5D=1"

# Test via FluentCRM's ?fluentcrm=1 auto-opt-in URL
curl -sS -L "$site/?fluentcrm=1&email=test%40test.com&first_name=Test" -o /dev/null
```

## Phase 5: Subscriber Creation (Verified Working)
```bash
# POST directly to FluentCRM REST API with admin credentials
curl -sS -X POST "$site/wp-json/fluent-crm/v2/subscribers" \
  -H "Authorization=[REDACTED] $B64" \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","first_name":"Test","lists":[1],"status":"subscribed"}'
# Returns 200 with created subscriber details
```

## Critical Issues to Flag
1. **Form dead**: `action="#"` with no JS handler — collects nothing
2. **Form broken**: redirect to `?fluentcrm=1` which just reloads homepage
3. **Zero integrations**: FluentCRM has no ESP/SMTP configured — zero emails will ever send
4. **Draft/empty sequences**: sequences exist but are draft status with empty bodies
5. **Duplicate lists**: same list created twice (check slug/title overlap)
6. **Published funnels with no content**: funnels trigger but email actions are empty
7. **Cloudflare blocks wp-login**: use REST API credentials instead

## Section 6: Email Form Remediation (Frontend JavaScript)

### Fix Dead Forms by Injecting JS Handler
When forms have `action="#"` with no JS handler, inject a script into page content:

```python
import json
# Get page content
r = requests.get(f"{site}/wp-json/wp/v2/pages/{page_id}?context=edit", headers={"Authorization": f"Basic {b64}"})
content = r.json()["content"]["raw"]

# Build JS form handler that POSTs to FluentCRM REST API
form_handler = '''
<script>
document.addEventListener("DOMContentLoaded", function() {
  var AFS_CRM = {
    api: "https://example.com/wp-json/fluent-crm/v2/subscribers",
    auth: "Basic BASE64_ENCODED_CREDENTIALS",
    subscribe: function(email, firstName, tags) {
      return fetch(this.api, {
        method: "POST",
        headers: { "Content-Type": "application/json", "Authorization": this.auth },
        body: JSON.stringify({ email: email, first_name: firstName || "", lists: [1], status: "subscribed", tags: tags || [] })
      }).then(function(r) { return r.json(); });
    }
  };

  // Fix subscribe form on page
  var subForm = document.querySelector(".your-form-class");
  if (subForm) {
    subForm.addEventListener("submit", function(e) {
      e.preventDefault();
      var email = subForm.querySelector('input[type="email"]').value;
      var name = subForm.querySelector('input[type="text"]').value || "";
      AFS_CRM.subscribe(email, name).then(function(data) {
        // Handle success/error
      });
    });
  }

  // Fix exit-intent form (dynamically created)
  var poll = setInterval(function() {
    var exitForm = document.getElementById("exit-form-id");
    if (exitForm && !exitForm.dataset.fixed) {
      exitForm.dataset.fixed = "1";
      exitForm.onsubmit = function(e) {
        e.preventDefault();
        var fd = new FormData(this);
        AFS_CRM.subscribe(fd.get("email"), fd.get("first_name"));
      };
    }
  }, 500);
});
</script>
'''

# Inject before existing script in page content
content = content.replace("</script>", form_handler + "</script>", 1)  # or other insertion point

# Update page
requests.post(f"{site}/wp-json/wp/v2/pages/{page_id}",
  headers={"Authorization": f"Basic {b64}", "Content-Type": "application/json"},
  json={"content": content})
```

**Security note**: Exposing FluentCRM REST API credentials in client-side JavaScript IS a security risk. Use this as a TEMPORARY fix until you can deploy a proper server-side proxy (mu-plugin, custom endpoint, or external form service).

## Section 7: FluentCRM Cron Fix

If automations show "56 years overdue" or never fire:

```bash
# Force run cron tasks
curl -sS -X POST "$site/wp-json/fluent-crm/v2/setting/run_cron" \
  -H "Authorization=[REDACTED] $B64" \
  -H "Content-Type: application/json" \
  -d '{"hook": "fluentcrm_scheduled_every_minute_tasks"}'

curl -sS -X POST "$site/wp-json/fluent-crm/v2/setting/run_cron" \
  -H "Authorization=[REDACTED] $B64" \
  -H "Content-Type: application/json" \
  -d '{"hook": "fluentcrm_scheduled_hourly_tasks"}'

# Verify cron status
curl -sS "$site/wp-json/fluent-crm/v2/setting/cron_status" \
  -H "Authorization=[REDACTED] $B64" -H "User-Agent: Mozilla/5.0"
```

If cron tasks still show as overdue after forcing:
- WordPress cron may be disabled in wp-config.php (`DISABLE_WP_CRON = true`)
- The site needs a server-side cron job: `wget -q -O - https://example.com/wp-cron.php?doing_wp_cron >/dev/null 2>&1`
- FluentCRM automations will NEVER fire until the cron is fixed

## Section 8: FluentCRM API Limitations (CRITICAL)

The following operations **CANNOT** be performed via FluentCRM REST API:
- **Updating sequences** — no route exists (`/wp-json/fluent-crm/v2/sequences/{id}` returns 404)
- **Updating funnel actions/steps** — save-funnel-sequences returns 404 via REST
- **Updating campaigns** — `update-single-campaign` requires "title" field, but POST may not work for updates
- **Reapplying funnels to existing subscribers** — works but returns message if no sequences found

Workarounds:
1. **For sequences**: Must be edited in wp-admin FluentCRM dashboard (Cloudflare blocks this)
2. **For campaigns**: Create new recurring campaigns via `/wp-json/fluent-crm/v2/recurring-campaigns`
3. **For forms**: Fix forms via JavaScript injection (see Section 6)
4. **For SMTP**: Must be configured in FluentSMTP settings via wp-admin dashboard

## Section 9: Complete Remediation Checklist

When email marketing is completely broken:

1. **Fix frontend forms** — inject JS handlers that POST to FluentCRM API → ✅ Immediate
2. **Force cron execution** — run overdue cron tasks via API → ✅ Immediate
3. **Check subscriber counts** — verify lists have subscribers → ✅ Via API
4. **Update sequences** — MUST be done in wp-admin dashboard → ⚠️ Manual
5. **Configure SMTP** — MUST be done in FluentSMTP settings → ⚠️ Manual
6. **Set SPF/DKIM/DMARC** — DNS records via Cloudflare → ⚠️ External
7. **Write email content** — sequence bodies need actual email copy → ⚠️ Manual

Items 4-7 require wp-admin access (blocked by Cloudflare) or DNS access.
Cannot be completed via REST API alone.

## Section 10: Multi-Site Custom Subscribe Route + Homepage Capture Pattern

For Alexiios-style sites, the winning remediation may not be FluentCRM-native. Several sites use active Code Snippets with custom REST subscribe routes and direct ESP delivery/debug endpoints. Prefer these existing site routes when present instead of exposing admin REST credentials in frontend JS.

Known route pattern examples from the 2026 audit/fix:
- FrenchyFab: `/wp-json/ffx/v1/subscribe`, debug `/wp-json/ffx/v1/enterprise-debug-v3`
- Mice Gone Guide: `/wp-json/mgg/v1/subscribe`, debug `/wp-json/mgg/v1/enterprise-debug-v3`
- Affiliate Marketing for Success: `/wp-json/amfs/v2/subscribe`, debug `/wp-json/amfs/v2/enterprise-debug-v3`
- Gear Up To Fit: `/wp-json/guf/v1/subscribe`, debug `/wp-json/guf/v1/enterprise-debug-v3`
- Gear Up To Grow: `/wp-json/gutg/v1/subscribe`, debug `/wp-json/gutg/v2/debug`
- Mystical Digits: `/wp-json/mdx/v1/subscribe`, debug `/wp-json/mdx/v1/enterprise-debug-v3`
- PlantasticHaven: `/wp-json/plantastic/v5/welcome-lead`, debug `/wp-json/plantastic/v5/mail-debug`
- EfficientGPTPrompts: `/wp-json/egp/v1/subscribe`, debug `/wp-json/egp/v1/debug`

### Reusable homepage capture deployment
When a homepage has no visible/working email capture, deploy a global Code Snippet named `Hermes Enterprise Email Capture UX` that only runs on `is_front_page()` / `is_home()` and injects:
- A scoped section `.hermes-lead-capture-2026`
- Responsive CSS scoped to that block only
- A `form.hermes-lead-form` that POSTs JSON to the site’s custom subscribe route
- No credentials in client JS

Use the Code Snippets REST API when available:
```bash
curl -sS "$site/wp-json/code-snippets/v1/snippets?context=edit" \
  -H "Authorization=[REDACTED] $B64" -H "User-Agent: Mozilla/5.0"

curl -sS -X POST "$site/wp-json/code-snippets/v1/snippets?context=edit" \
  -H "Authorization=[REDACTED] $B64" -H "Content-Type: application/json" \
  --data-binary @payload.json
```
Then activate if needed:
```bash
curl -sS -X POST "$site/wp-json/code-snippets/v1/snippets/$ID/activate" \
  -H "Authorization=[REDACTED] $B64" -H "User-Agent: Mozilla/5.0"
```

### Verification contract for this pattern
Use Node Playwright from `/home/hermes/.hermes/hermes-agent/node_modules/playwright` if Python Playwright is missing. Verify every site:
1. Homepage loads and `form.hermes-lead-form input[type=email]` is visible on desktop.
2. Same form/input is visible on mobile.
3. Desktop and mobile `documentElement.scrollWidth - innerWidth` are below a small tolerance.
4. Submit a controlled test email (`papalexios+prefix-timestamp@gmail.com`) by dispatching a JS submit event instead of relying on Playwright `.click()` when layout animations make buttons unstable.
5. Capture the frontend network response to the custom `/wp-json/.../subscribe` or `welcome-lead` route and require HTTP 200 plus `ok:true`, `success:true`, `subscribed`, or the site’s success message.
6. Query the site’s authenticated debug route with the tested email, where supported, and require delivery evidence such as `status:201`, `sent:true`, `result:true`, or `messageId`.

### Pitfalls discovered
- Do not use frontend JavaScript that references `f.email`; some browsers/forms do not expose controls as form properties reliably. Use `form.querySelector('input[type=email]').value`.
- For same-site routes, absolute REST URLs can be more reliable than relative `/wp-json/...` URLs when optimization plugins rewrite or defer scripts.
- On AffiliateMarketingForSuccess, a dynamic config-based snippet sometimes left the button stuck at `Sending…` with no network request. A simpler static snippet using `form.onsubmit = function(...) { fetch('https://affiliatemarketingforsuccess.com/wp-json/amfs/v2/subscribe', ...) }` fixed it.
- Playwright `.click()` can time out on animated/unstable buttons (observed on GearUpToFit). Dispatching `new Event('submit', {bubbles:true,cancelable:true})` from page JS is a better verification method for form functionality.
- Some existing forms are intentionally hidden/sticky widgets; verify visible form count, not total email inputs.

## Important Notes (Updated)
- FluentCRM `/wp-json/fluent-crm/v2/setting` returns empty JSON `{"__bench":1.5}` — this is normal for non-admin-level REST auth
- FluentCRM `/wp-json/fluent-crm/v2/setting/integrations` returns `{"integrations":[]}` when empty
- Subscriber creation via POST to `/wp-json/fluent-crm/v2/subscribers` **does work** with admin REST API credentials
- Cloudflare blocks wp-login (`wp-login.php` returns 403 challenge) — use REST API only
- FluentForm `/fluentform/v1/forms` requires higher privileges than REST API provides
- FluentCRM forms are created with POST to `/wp-json/fluent-crm/v2/forms` requiring: `title`, `template_id`, `selected_list` (map), `selected_tags` (map)
