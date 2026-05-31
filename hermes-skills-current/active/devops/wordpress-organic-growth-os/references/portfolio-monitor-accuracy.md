# Portfolio SEO/GEO/AEO monitor accuracy notes

Use this when building or interpreting portfolio-wide WordPress SEO/AI-visibility monitors.

## H1 counting pitfall

HTML parsers may deliver a single `<h1>` as multiple text chunks when inline spans, line breaks, or hero animations split the text. Do not count each text chunk as a separate H1.

Correct approach:

1. On `<h1>` start: set `in_h1=true` and start a buffer.
2. On text/data events while `in_h1`: append to the buffer.
3. On `</h1>`: normalize whitespace, append one completed H1 record, and clear the buffer.

This avoids false positives such as split hero headings like `Gear / up / to` or `Prompts engineered / for / operators` being counted as multiple H1s.

## Sitemap status pitfall

Do not flag `/sitemap.xml` alone as a failure on Yoast/WordPress sites if `/sitemap_index.xml` is 200 and robots.txt points to a valid sitemap. Many healthy WordPress stacks use `sitemap_index.xml` as canonical.

Recommended logic:

- `/robots.txt` should be 200.
- At least one known sitemap endpoint should be 200: `/sitemap.xml` OR `/sitemap_index.xml` OR the sitemap URL advertised in robots.txt.
- Flag only when all sitemap sources fail or contradict the canonical sitemap surface.

## Priority framing

For portfolio-wide growth passes, separate:

- monitor/parser false positives,
- true technical SEO defects,
- content-quality/topical-authority opportunities,
- deployment blockers.

Do not spend execution budget fixing false positives; patch the monitor first, rerun, then prioritize remaining true anomalies.