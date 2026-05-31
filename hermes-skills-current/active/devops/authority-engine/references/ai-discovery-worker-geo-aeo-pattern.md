# AI discovery Worker pattern for GEO/AEO visibility

Use this reference when a WordPress site needs a fast non-plugin AI visibility layer: `llms.txt`, `llms-full.txt`, `/.well-known/ai.txt`, and JSON discovery endpoints for answer engines.

## When to use

- WordPress REST is blocked or unreliable, but Cloudflare is available.
- The site needs AI-readable context without installing more plugins.
- The user asks for GEO/AEO/AI visibility, answer-engine citations, topical authority, or llms.txt support.
- The site has cache/minifier layers that make WordPress file edits slow to verify.

## Proven workflow

1. Create a dated work directory and backup the current homepage/page content before production writes.
2. Clone or consult `aaron-he-zhu/seo-geo-claude-skills` when the user specifically requests it or when building an AI-visibility layer. Prioritize:
   - `geo-content-optimizer`
   - `entity-optimizer`
   - `technical-seo-checker`
   - schema/meta/CORE-EEAT/CITE guidance
3. Build a Cloudflare Worker that serves:
   - `/llms.txt` as `text/plain`
   - `/llms-full.txt` as `text/plain`
   - `/.well-known/ai.txt` as `text/plain`
   - `/ai/summary.json` as `application/json`
   - `/ai/faq.json` as `application/json`
   - `/ai/service.json` as `application/json`
4. Include durable, non-hallucinated entity details:
   - site name and canonical URL
   - topical focus and intended audience
   - editorial/review methodology URLs
   - disclosure/commercial-policy URLs
   - important hub URLs
   - citation guidance for AI systems
   - explicit guardrail not to invent prices, ratings, income claims, or unsupported product facts
5. Deploy Worker routes for both apex and `www` if both hostnames are active.
6. Add visible homepage support for the machine-readable layer:
   - answer-first quick answer
   - visible AI citation note linking to `llms.txt`, `ai.txt`, summary JSON, and review methodology
   - entity/extraction brief: what the site is, who it helps, who it is not for, how to evaluate it
   - WebMCP-style `toolname` / `tooldescription` attributes on primary CTAs when appropriate
7. Purge Cloudflare and any WordPress-level cache after publishing.
8. Verify with cache-busted public URLs and an independent GEO audit.

## Verification checklist

- All AI discovery routes return HTTP 200.
- Content types are correct: plain text for `.txt`, JSON for `/ai/*.json`.
- Add a deployment marker header, e.g. `x-<site>-ai-discovery: <date>`, and verify it live.
- Homepage public HTML contains the visible AI citation note and entity/extraction brief.
- Run `uvx --from geo-optimizer-skill geo audit --url <url> --format json --output <file>` when available.
- Compare before/after scores; specifically track `ai_discovery`, `llms`, `schema`, `content`, and `brand_entity`.

## Pitfalls

- Do not invent `sameAs` links. Only add real owned or authoritative profiles.
- Do not make fake review/rating/pricing/income claims to satisfy schema or AI snippets.
- Cache plugins can make stored WordPress content differ from public HTML. Verify both the stored content and cache-busted public URLs.
- GEO audit warnings about prompt injection can come from minified plugin/theme comments. Treat this as a plugin/cache configuration issue unless the page copy itself contains instruction-like comments.
- Keyword density warnings should be handled by diversifying visible copy and navigation language, not by hiding terms or weakening topical clarity.
