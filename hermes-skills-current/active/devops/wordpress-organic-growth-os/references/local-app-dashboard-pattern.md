# Local App Dashboard Pattern for Organic Growth OS

Use this when the user asks for an “app,” “dashboard,” “OS,” “command center,” or says “where do I see all this?” after OS artifacts are created.

## Durable lesson
Do not stop at folders, Markdown files, scripts, or cron jobs. The user expects a visible, easy-to-open app surface.

## Minimum viable local app
Create or refresh:
- `index.html` in `/home/hermes/.hermes/organic-growth-os/`
- links to latest visual dashboard, Markdown dashboard, command center, playbooks, and per-site state files
- a premium responsive UI with site cards and clear CTAs
- exact browser URL in the final reply

## Server pattern
Start a local static server from the OS root when the user wants to view it now:

```bash
cd /home/hermes/.hermes/organic-growth-os
python3 -m http.server 8787 --bind 0.0.0.0
```

Then verify both:
- `http://127.0.0.1:8787/`
- `http://127.0.0.1:8787/dashboards/portfolio-dashboard-latest.html`

## Final response pattern
Lead with the app URL, not implementation detail:

- Main app: `http://localhost:8787/`
- Visual dashboard: `http://localhost:8787/dashboards/portfolio-dashboard-latest.html`
- Explain briefly whether it is a static local app or a full interactive SaaS-style admin app.
- If static, offer the next upgrade path: forms, buttons, live WP actions, approval gates, GSC/Bing/GA4 integrations, charts, and monetization tracker.

## Pitfall
A technically correct “OS” made of artifacts still feels invisible if there is no browsable entry point. For this user, visible premium UI is part of the deliverable whenever the wording includes “app,” “beautiful,” “modern,” or “easy to use.”
