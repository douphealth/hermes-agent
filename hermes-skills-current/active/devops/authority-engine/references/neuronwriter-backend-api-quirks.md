# NeuronWriter backend API quirks for WordPress rewrite workflows

Use this when automating NeuronWriter setup/scoring for WordPress rewrite batches, especially when browser interaction is slow or brittle.

## Session/login pattern

- Login form posts to `https://app.neuronwriter.com/ucp/login` with form fields:
  - `email`
  - `password`
  - optional `remember-me`
- A successful login redirects to `/` and sets a `contai_session_id` cookie.
- Fetching `/` with that cookie should return a dashboard page titled like `Dashboard | NEURONwriter - powered by CONTADU`.

## Project discovery

- Dashboard/project pages expose project signatures in links like:
  - `/project/view/<project_sig>`
- For an existing project page, the optimisation route is commonly:
  - `https://app.neuronwriter.com/project/view/<project_sig>/optimisation`

## Creating a new analysis

Endpoint:

```text
POST https://app.neuronwriter.com/backend/new-analysis
Content-Type: application/json
Referer: https://app.neuronwriter.com/project/view/<project_sig>/optimisation
```

Payload shape observed from page JS:

```json
{
  "project": "<project_sig>",
  "is_multiple_analysis": 0,
  "keyword": "affiliate marketing strategy",
  "multiple_keywords": "",
  "custom_competitors": "",
  "additional_keywords": "affiliate strategy\naffiliate marketing plan",
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

Successful response example:

```json
{"status":"ok","analysis_sig":"ede02355589bc9a2","opportunity_id":null}
```

## Durable pitfalls

- `language` must be a full language name like `English`, not an ISO code like `en`. If wrong, NeuronWriter returns a long `Language not supported` error.
- `additional_keywords` must be newline-separated, one keyword per line. Comma-separated values can be rejected with an error about disallowed characters and/or “Enter one keyword per each line.”
- `engine` values are Google host strings like `google.com`, matching the project/search target.
- Treat NeuronWriter analysis creation as setup only; do not claim the rewrite was scored 90+ until content has been loaded/scored in the analysis and the score evidence is captured.

## Suggested workflow checkpoint

Before rewriting/publishing WordPress content:

1. Back up the raw WP post content and metadata.
2. Create or locate the NeuronWriter analysis for the exact target URL + primary keyword.
3. Save the `analysis_sig` next to the WP post ID.
4. Rewrite against the terms/outline, then score/tune until verified 90+.
5. Publish only after score evidence and content QA are captured.
