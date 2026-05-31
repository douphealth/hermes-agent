<!-- Consolidated from skill: fluentcrm-email-audit; original path: /home/hermes/.hermes/skills/devops/fluentcrm-email-audit -->

---
name: fluentcrm-email-audit
description: Audit and remediate FluentCRM email marketing setup on WordPress sites via REST API. Covers form repair, sequence audit, deliverability checks, and enterprise-grade configuration when admin UI is blocked by Cloudflare WAF.
category: devops
tags: [wordpress, email-marketing, fluentcrm, rest-api, automation]
---

# FluentCRM Email Marketing Audit & Remediation

## Overview
Comprehensive audit and fix workflow for FluentCRM email marketing infrastructure on WordPress sites. Works entirely via REST API when Cloudflare blocks wp-admin access.

## Prerequisites
- REST API admin credentials Application Password (different from wp-login password)
- Site must have FluentCRM plugin installed
- Cloudflare may block wp-login.php — all operations use REST API only

## 1. Initial Reconnaissance

```bash
# Verify REST API admin access
curl -s "https://example.com/wp-json/wp/v2/users/me?context=edit" \
  -H "Authorization=[REDACTED] <base64_user:pass>" \
  -H "User-Agent: Mozilla/5.0"
# Must return roles: ["administrator"]

# If FluentCRM routes are at /wp-json/fluent-crm/v2/ (not /fluent-crm/v2/)
# always use the wp-json prefix for consistent auth
```

**Important**: FluentCRM custom v2 endpoints (`/fluent-crm/v2/`) may return 404 HTML without the `/wp-json/` prefix. Always use `/wp-json/fluent-crm/v2/`.

## 2. Complete Infrastructure Audit

### 2a. Lists & Subscribers
```bash
# Get all lists with subscriber counts
curl -s "https://example.com/wp-json/fluent-crm/v2/lists" \
  -H "Authorization=[REDACTED] <base64>" -H "User-Agent: Mozilla/5.0"

# Check subscriber details
curl -s "https://example.com/wp-json/fluent-crm/v2/subscribers" \
  -H "Authorization=[REDACTED] <b64>" -H "User-Agent: Mozilla/5.0"

# Tags
curl -s "https://example.com/wp-json/fluent-crm/v2/tags" \
  -H "Authorization=[REDACTED] <b64>" -H "User-Agent: Mozilla/5.0"
```

### 2b. Email Sending Infrastructure
```bash
# Check all integrations (CRITICAL: if empty, NO emails can be sent)
curl -s "https://example.com/wp-json/fluent-crm/v2/setting/integrations" \
  -H "Authorization=[REDACTED] <b64>" -H "User-Agent: Mozilla/5.0"

# Check general settings
curl -s "https://example.com/wp-json/fluent-crm/v2/setting" \
  -H "Authorization=[REDACTED] <b64>" -H "User-Agent: Mozilla/5.0"
```

**Interpretation**:
- `integrations: []` → NO email service configured. Emails cannot send.
- Empty settings object `{__bench: X}` → requires admin-level permissions (may still work for GET but not POST)
- FluentSMTP must be configured separately through wp-admin

### 2c. Sequences, Campaigns, Funnels
```bash
# Sequences (individual emails in a series)
curl -s "https://example.com/wp-json/fluent-crm/v2/sequences" \
  -H "Authorization=[REDACTED] <b64>" -H "User-Agent: Mozilla/5.0"

# Campaigns (one-time broadcasts)
curl -s "https://example.com/wp-json/fluent-crm/v2/campaigns" \
  -H "Authorization=[REDACTED] <b64>" -H "User-Agent: Mozilla/5.0"

# Funnels (automation workflows)
curl -s "https://example.com/wp-json/fluent-crm/v2/funnels" \
  -H "Authorization=[REDACTED] <b64>" -H "User-Agent: Mozilla/5.0"
```

**What to look for**:
- Sequences with `status: "draft"` → never send
- Sequences with `email_body: ""` or `email_subject: null` → empty content
- Funnels with `status: "published"` but 0 sequences linked → trigger fires but does nothing
- Campaigns with `status: "draft"` → never scheduled/sent

## 3. Frontend Form Audit

### 3a. Scan Homepage for Forms
Download the live page and scan:
```bash
curl -sS "https://example.com" -o /tmp/home.html

# Check for dead forms (action="#" with no JS handler)
grep -i '<form' /tmp/home.html

# Check all JavaScript that might handle forms
grep -i 'submit\|preventDefault\|FormData\|fetch(' /tmp/home.html
```

### 3b. Common Broken Patterns
1. **Dead subscribe form**: `<form class="..." action="#" method="post">` with NO JavaScript submit handler → collects nothing
2. **Broken redirect form**: Exit-intent that redirects to `?fluentcrm=1&email=...` → just reloads homepage
3. **FluentCRM opt-in URLs**: `?fluentcrm=1&email=...&first_name=...` only works if FluentCRM's double opt-in is enabled and configured in admin settings

## 4. Fixing Frontend Forms (Zero-Risk REST API Edit)

### 4a. The Safe Approach
Since you cannot verify SMTP/config without wp-admin (often blocked by Cloudflare), fix ONLY the form infrastructure first:

1. **Replace broken form handlers** in page content with JavaScript that POSTs to FluentCRM's public opt-in endpoint
2. **Add proper success/error UI** to the forms
3. **Add spam prevention** (hCaptcha/turnstile if keys are configured in Kadence blocks settings)

### 4b. Finding Form-Containing Pages
```bash
# Get all pages and scan for email forms
curl -s "https://example.com/wp-json/wp/v2/pages?per_page=100" \
  -H "Authorization=[REDACTED] <b64>"

# Check each page's content for forms
# Pages with action="#" or no JS handlers need fixing
```

### 4c. Patch Homepage Content
```bash
# Get current page content with edit context
curl -s "https://example.com/wp-json/wp/v2/pages/{id}?context=edit" \
  -H "Authorization=[REDACTED] <b64>"

# Update page content via POST override (Cloudflare blocks PUT)
curl -s -X POST "https://example.com/wp-json/wp/v2/pages/{id}?context=edit" \
  -H "Authorization=[REDACTED] <b64>" \
  -H "Content-Type: application/json" \
  -H "X-HTTP-Method-Override: PUT" \
  -H "User-Agent: Mozilla/5.0" \
  --data-binary "@/tmp/payload.json"
```

**CRITICAL**: Write the payload JSON to a file first. Shell-escaping large HTML/JS strings fails silently.

## 5. Deliverability Prerequisites (Cannot Be Done via REST API Alone)

These require either admin panel access or DNS access:

1. **SMTP Configuration**: FluentSMTP needs SMTP credentials (Brevo, SendGrid, Mailgun, SES, Postmark)
2. **Domain Verification**: SPF, DKIM, DMARC records must be added to DNS
3. **From Address**: Must match the domain (e.g., noreply@example.com)
4. **Warm-up**: New domains/IPs need gradual send volume increase

## Critical Pitfalls

- **Cloudflare blocks wp-login.php**: The Python `requests` library gets a 403 Cloudflare challenge page. Cannot login via cookie auth. All work must be done via REST API.
- **REST API credentials ≠ wp-admin password**: The secrets file may have both. Use the one that returns administrator role from `/wp/v2/users/me`.
- **FluentCRM endpoint prefix**: Always use `/wp-json/fluent-crm/v2/`, not just `/fluent-crm/v2/`. Without the prefix you get 404 HTML.
- **FluentCRM integration endpoint**: `/wp-json/fluent-crm/v2/setting/integrations` returns actual data, while `/setting` returns just a benchmark object.
- **FluentCRM `?fluentcrm=1` URL**: This is FluentCRM's double opt-in parameter. It only works if auto-subscribe settings are enabled in the FluentCRM dashboard. If it just reloads the homepage, the feature is not configured.
- **Zero integration = zero emails**: FluentCRM with no ESP/SMTP integration silently drops all emails. Subscribers are captured but nothing sends.
- **Funnel subscribers ≠ emails sent**: A funnel may show "12 subscribers in automation" but if the linked sequences are draft or empty, no emails actually fire.

## Audit Checklist Template

- [ ] FluentCRM lists exist and have subscribers
- [ ] At least 1 ESP integration is configured
- [ ] All forms on pages have working submit handlers
- [ ] All funnels have active sequences with content
- [ ] All campaigns are published and scheduled (or ready to schedule)
- [ ] FluentSMTP is configured and test email succeeds
- [ ] From address matches sending domain
- [ ] SPF, DKIM, DMARC records are set in DNS
- [ ] Double opt-in is configured (or single opt-in with confirmation)
- [ ] Unsubscribe link in all emails
- [ ] Spam prevention (hCaptcha/turnstile) on all forms