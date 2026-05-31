# GearUpToFit lead-capture audit pattern

Use when checking whether GearUpToFit has real lead capture, newsletter capture, or CRM/list integration.

## Public crawl checks

Check high-value live pages, not only old WordPress pages:

- `https://gearuptofit.com/` — current Worker/Lovable homepage
- `/shoe-finder/`
- `/shoe-match/`
- `/free-fitness-plan/`
- `/contact/`
- category hubs: running, review, nutrition, health, weight-loss
- legacy pages only as secondary evidence: `/home-gearuptofit/`, `/gearuptofit/`

For each URL inspect:

```bash
curl -sS -L "$URL" | grep -Eio '<form\b|type=["'"']email|newsletter|subscribe|mailchimp|convertkit|mailerlite|hubspot|brevo|fluent|wpforms|elementor-form|popup|lead|download|ebook' | head -50
```

If Python dependencies are minimal, avoid assuming BeautifulSoup exists; use regex/html stdlib or install deliberately only if needed.

## Browser checks

Curl can miss JS-rendered forms and popups. Browser-check the live page after load and after scroll:

```js
({
  url: location.href,
  forms: [...document.forms].map(f => ({
    name: f.getAttribute('name'),
    cls: f.className,
    action: f.action,
    inputs: [...f.querySelectorAll('input,textarea,select,button')].map(i => ({
      tag: i.tagName,
      type: i.type,
      name: i.name,
      placeholder: i.placeholder,
      text: i.innerText || i.value,
      visible: !!(i.offsetWidth || i.offsetHeight)
    }))
  })),
  emailInputs: [...document.querySelectorAll('input[type=email], input[name*=email i], input[placeholder*=email i]')].map(i => ({
    name: i.name,
    placeholder: i.placeholder,
    visible: !!(i.offsetWidth || i.offsetHeight)
  })),
  popupTriggers: [...document.querySelectorAll('a[href*=popup], [class*=popup i], [role=dialog]')].slice(0,20).map(e => ({
    tag: e.tagName,
    text: e.innerText,
    href: e.href,
    visible: !!(e.offsetWidth || e.offsetHeight)
  }))
})
```

## WordPress/Elementor backend checks

Use REST `context=edit` with app-password credentials from the local secrets file. Do not print secrets.

Check active plugins and Elementor data:

- `/wp-json/wp/v2/plugins`
- `/wp-json/wp/v2/elementor_library?per_page=100&context=edit`
- `/wp-json/wp/v2/pages?per_page=100&context=edit`
- `/wp-json/wp/v2/elementor_snippet?per_page=100&context=edit`

Look for dedicated lead/CRM plugins and integrations:

- Mailchimp for WordPress, ConvertKit, MailerLite, Brevo, HubSpot, ActiveCampaign
- Fluent Forms, WPForms, Gravity Forms
- FluentCRM or other local CRM plugins
- Elementor Pro Form widgets with `submit_actions`, integrations, or database saving

For Elementor form widgets, parse `_elementor_data` and report:

- `form_name`
- `form_fields`
- `button_text`
- `submit_actions`
- `email_to`
- `mailchimp_fields_map`, `convertkit_fields_map`, `mailerlite_fields_map`
- success/error messages

## Interpretation rules

- A search form is not lead capture.
- A contact form is contact capture, not newsletter/marketing lead capture.
- A visible email input that only sends to `admin@admin.admin` is weak/broken lead capture until a real destination is confirmed.
- Empty Mailchimp/ConvertKit/MailerLite field maps mean the Elementor form is not integrated with those providers, even if those words appear in serialized defaults.
- Legacy pages with newsletter forms do not prove the current live homepage captures leads, especially when the apex homepage is served by a Cloudflare Worker/Lovable app.
- High-value SEO/app pages should be checked specifically: `/shoe-finder/`, `/shoe-match/`, and `/free-fitness-plan/` are priority surfaces.

## GearUpToFit signals observed May 2026

- Current apex homepage had no forms/email inputs in browser.
- `/shoe-finder/` and `/shoe-match/` had no email capture; `/shoe-finder/` only had search and a non-lead Elementor popup trigger.
- `/contact/` had an Elementor contact form, but destination was `admin@admin.admin`.
- Legacy `/home-gearuptofit/` had a `Homepage Newsletter` Elementor form with email field and `Join Free`, but provider maps were empty and destination was `admin@admin.admin`.
- Active relevant plugins were Elementor and Elementor Pro; no dedicated email marketing/CRM plugin was evident via REST plugin listing.
