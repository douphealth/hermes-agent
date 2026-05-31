# AMFS Public SEO/GEO/AEO Baseline

Session-specific reference for `affiliatemarketingforsuccess.com` discovered during a public Supercharger reconnaissance. Use as starting context only; re-verify live before editing or making claims.

## Site identity

- Domain: `https://affiliatemarketingforsuccess.com/`
- WordPress + Yoast site.
- Publisher focus: affiliate marketing, affiliate SEO, affiliate programs, affiliate tools, AEO/GEO/AI visibility, email monetization, content strategy, reviews/comparisons.
- Primary public sitemap: `https://affiliatemarketingforsuccess.com/sitemap_index.xml`
- Key sitemap children observed:
  - `/post-sitemap.xml`
  - `/page-sitemap.xml`
  - `/category-sitemap.xml`
  - `/afs-live-posts-supplemental-sitemap.xml`

## Verified public signals from the session

- Homepage: `200`, canonical self-reference, index/follow robots meta.
- Yoast metadata and Yoast sitemap output visible publicly.
- WordPress REST API reachable publicly for post/page metadata samples.
- `/robots.txt`: `200`, explicitly allows major AI/citation crawlers including GPTBot, ChatGPT-User, OAI-SearchBot, ClaudeBot, PerplexityBot, Bingbot, Applebot, CCBot.
- `/llms.txt`: `200`, Yoast-generated, around 318 words in audit output.
- `/llms-full.txt`: `200`, redirected to an uploads-hosted text file.
- Enterprise GEO/AEO audit homepage score observed: `72/100`, band `good`.
- CDN: Cloudflare. Audit bot checks for GPTBot, ClaudeBot, PerplexityBot returned `200` and were not blocked.
- Raw HTML was crawlable without JavaScript; audit saw roughly 1,800 words and 48 headings.

## High-leverage gaps observed

- AI discovery endpoints missing or weak:
  - `/.well-known/ai.txt`
  - `/ai/summary.json`
  - `/ai/faq.json`
  - `/ai/service.json`
- Searchstack llms check reported sitemap does not reference `llms.txt` / `llms-full.txt`.
- llms audit warning: H1 should be first line of `llms.txt`.
- Several major hub pages exposed via REST had Yoast titles but null Yoast meta descriptions in the sampled output:
  - `/email-monetization-hub/`
  - `/affiliate-content-strategy-hub/`
  - `/aeo-geo-hub/`
  - `/affiliate-tools-hub/`
  - `/affiliate-programs-hub/`
  - `/affiliate-seo-hub/`
  - `/affiliate-marketing-hub/`
  - `/content-strategy-guide/`
  - `/start-here/`
- Homepage entity/trust hardening opportunities:
  - stronger Organization sameAs/entity links where real
  - homepage as canonical brand/entity overview
  - clearer routing to review methodology, disclosure, AI/content policy, Start Here, and pillar hubs
- Review/comparison posts should preserve commercial trust modules: disclosure, methodology/date checked, best for/not best for, alternatives, pricing/source caveats, rel sponsored/nofollow where relevant.

## Audit artifact paths from this session

These were generated in `/tmp` and are not durable; use as examples of expected artifact names, not as permanent storage:

- `/tmp/amfs-enterprise-geo-aeo/geo-audit-url.json`
- `/tmp/amfs-enterprise-geo-aeo/geo-audit-sitemap.json`
- `/tmp/amfs-enterprise-geo-aeo/llms.txt`
- `/tmp/amfs-enterprise-geo-aeo/.searchstack.toml`

## Operational lessons

- The bundled public WordPress audit and enterprise GEO/AEO runner may take longer than default timeouts on AMFS because the sitemap is large; if a full run times out, inspect partial artifacts and continue with targeted checks rather than declaring failure.
- For domain-only intake, run a site-level audit wave first rather than asking for a single post URL. Then offer the user the next execution mode: site audit, homepage/hub draft upgrades, or WordPress draft implementation.
- Do not claim rankings, traffic, GSC movement, AI citations, or search volume without first-party GSC/Searchstack/API evidence.
