# NeuronWriter backend automation notes

Use when a WordPress SEO rewrite must be tuned to NeuronWriter score targets without relying on manual browser-only workflows.

## Analysis creation

A NeuronWriter project page can reveal the project signature and existing analysis signatures. For AMFS, the project signature observed in-session was `de592047df7acdd5`.

Create a new analysis with session cookies by posting to:

```text
POST https://app.neuronwriter.com/backend/new-analysis
```

Payload shape:

```json
{
  "project": "PROJECT_SIG",
  "is_multiple_analysis": 0,
  "keyword": "primary keyword",
  "multiple_keywords": "",
  "custom_competitors": "",
  "additional_keywords": "keyword one\nkeyword two\nkeyword three",
  "target_url": "https://example.com/path/",
  "engine": "google.com",
  "language": "English",
  "prefer_lang": 1,
  "update_inventory": 0,
  "assigned_to": "",
  "deadline": "",
  "geolocation_mode": "",
  "geolocation": ""
}
```

Pitfalls:

- `language` must be the UI label `English`; `en` can fail or produce unusable behavior.
- `additional_keywords` should be newline-separated.
- Save the JSON response and resulting analysis signature as evidence.

## Score bridge pattern

- Fetch the editor page for an analysis and scrape/parse the JS data needed for terms, title/meta targets, and scoring endpoints.
- Send draft body text plus title/meta description to the backend scoring/readability endpoints rather than estimating score by keyword count.
- Save raw score JSON (`overall_score`, parts, word count, readability, matched terms) before publishing.
- Treat score ≥ target as one checkpoint only; still run WordPress stored-content, public raw HTML, and rendered/browser verification.

## Content quality guardrails

- NeuronWriter scoring pressure can encourage repetition. Keep exact terms where needed, but use them in useful sections/checklists and avoid machine-like keyword stuffing.
- Do not use NeuronWriter optimization to preserve or amplify unsupported claims. Remove or source claims first, then tune.
