---
name: wordpress-email-marketing-operations
description: Use when auditing, repairing, replacing, or hard-cutting WordPress email marketing systems across FluentCRM, FluentSMTP, FluentForms, MailPoet, Brevo, Kadence/ESP integrations, signup forms, automations, reply paths, and deliverability when wp-admin may be blocked by Cloudflare.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [wordpress, email, fluentcrm, mailpoet, brevo, deliverability, rest-api]
    related_skills: [wp-rest-cloudflare, authority-engine]
---

# WordPress Email Marketing Operations

## Overview

This is the umbrella skill for WordPress email-marketing infrastructure work: audits, form repairs, FluentCRM/FluentSMTP diagnosis, MailPoet fixes, Brevo hard-cuts, branded reply-path verification, and REST-based remediation when wp-admin is unavailable.

The old one-session skills are preserved as reference files under `references/`. Load those references when a task matches a narrow provider or failure mode.

## When to Use

- A WordPress newsletter/signup/lead magnet form is broken, silently failing, or connected to the wrong provider.
- FluentCRM, FluentSMTP, FluentForms, MailPoet, Brevo, Kadence, Mailchimp, or legacy widgets need audit or replacement.
- Old automations continue sending stale emails or wrong reply-to headers after a migration.
- Cloudflare blocks wp-admin but REST API credentials or app passwords still work.
- You need to verify end-to-end email delivery, headers, sender identity, unsubscribe behavior, sequence state, and lead capture.

Do not use for generic content SEO unless email capture or lead routing is part of the task.

## Operating Model

1. **Map the live capture surface.** Fetch homepage and relevant pages, then search rendered and REST content for `type="email"`, form actions, Fluent/MailPoet/Brevo widgets, script embeds, and shortcodes.
2. **Inventory provider state.** Enumerate lists, tags, forms, funnels/sequences, campaigns, SMTP settings, cron health, and recent submissions through REST/API endpoints where possible.
3. **Find the actual send path.** Do not assume the visible form owns delivery. Trace handler code, plugin hooks, snippets, webhooks, transactional SMTP, and direct-provider APIs.
4. **Choose the smallest safe intervention.** Repair handler bugs when the current stack is sound; hard-cut to direct Brevo or another known-good path when legacy automation leakage is persistent.
5. **Disable stale automations explicitly.** Archive, pause, or bypass old funnels so old copy/reply-to headers cannot keep leaking.
6. **Verify with evidence.** Submit a controlled test, inspect subscriber/list/tag changes, confirm the exact email body and headers received, and check logs/API status.

## Provider-Specific Subsections

### FluentCRM / FluentSMTP / FluentForms

- Prefer REST/API inspection when wp-admin is blocked.
- Audit forms, lists, tags, funnels, sequences, campaigns, SMTP sender, and cron.
- Verify both CRM state and received email; CRM success does not prove delivery.
- Watch for Cloudflare path differences and endpoint prefixes.

Reference files:
- `references/fluentcrm-email-audit.md`
- `references/wordpress-fluentcrm-email-audit-fix.md`
- `references/wp-email-audit.md`
- `references/wordpress-fluentcrm-brevo-cutover-hardcut.md`

### MailPoet

- MailPoet 5.x API crashes may require replacing a PHP handler with REST/AJAX rather than trying to keep the broken path alive.
- A frontend success message is not proof of subscription or delivery.
- Verify actual MailPoet subscriber state and the SMTP/plugin layer.

Reference file: `references/mailpoet-subscribe-fix.md`

### Brevo hard-cut / direct delivery

- Use when legacy FluentCRM/Brevo routes keep sending wrong welcome emails or reply-to headers.
- Build an explicit direct-send helper, disable old automations, and verify branded From/Reply-To headers in a real mailbox.
- Treat empty `200` frontend responses as a separate UI/JS bug from provider delivery.

Reference files:
- `references/wordpress-brevo-sequence-hardcut.md`
- `references/wordpress-fluentcrm-brevo-cutover-hardcut.md`

## Verification Checklist

- [ ] Live page/form source inspected, not just plugin assumptions.
- [ ] Provider lists/tags/forms/funnels/sequences inventoried.
- [ ] Handler path identified and stale automations disabled or bypassed.
- [ ] Controlled test submission performed.
- [ ] Subscriber/contact state verified in the provider.
- [ ] Received message body, sender, reply-to, and timing verified.
- [ ] Final report includes exact endpoints/actions used and evidence.

## Common Pitfalls

1. **Trusting UI success text.** Always verify provider state and mailbox receipt.
2. **Fixing only one layer.** WordPress forms, CRM automations, SMTP, and provider APIs can each be independently broken.
3. **Leaving old funnels active.** Migrations fail when stale sequences continue to fire.
4. **Ignoring headers.** Branded reply-path and From/Reply-To correctness matter as much as delivery.
5. **Assuming wp-admin is required.** REST/app-password access often works when Cloudflare blocks the admin UI.


## Consolidated Reference Index

The following formerly separate narrow skills have been absorbed into this umbrella. Load the listed reference file only when that specific provider, failure mode, or workflow detail is needed.

- `fluentcrm-email-audit` → `references/fluentcrm-email-audit.md`
- `mailpoet-subscribe-fix` → `references/mailpoet-subscribe-fix.md`
- `wordpress-brevo-sequence-hardcut` → `references/wordpress-brevo-sequence-hardcut.md`
- `wordpress-fluentcrm-brevo-cutover-hardcut` → `references/wordpress-fluentcrm-brevo-cutover-hardcut.md`
- `wordpress-fluentcrm-email-audit-fix` → `references/wordpress-fluentcrm-email-audit-fix.md`
- `wp-email-audit` → `references/wp-email-audit.md`
