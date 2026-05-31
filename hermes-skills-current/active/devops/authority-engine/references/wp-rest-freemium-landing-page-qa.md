# WordPress REST freemium landing-page build + QA notes

Use when creating main-domain SEO landing pages that route to freemium apps/calculators/planners on subdomains.

## Proven build pattern
- Create one main-domain SEO page per app with a clear slug and canonical URL; keep the app on its subdomain as the conversion destination.
- Structure the page as: hero answer/benefit + primary CTA, app preview card, answer-first explanation, semantic coverage section, how-the-app-works steps, trust/safety boundaries, internal topical links, FAQ, final CTA.
- Add schema as JSON-LD where allowed: `WebPage`, `SoftwareApplication`, `FAQPage`, and `BreadcrumbList`.
- Use a single true HTML `<h1>` in source. If the theme injects the page title as H1, make the custom hero title a styled non-H1 or visually suppress the theme title and keep the custom H1.
- Keep public copy reader-first: entities and keywords should appear naturally in headings/body/FAQ/schema/internal anchors, not as raw keyword dumps.

## REST publishing details
- Use WordPress REST/direct POST when admin is blocked by Cloudflare.
- Use WordPress-safe HTML blocks/wrappers if Gutenberg strips markup.
- If CSS/schema/head is stripped, move it into an active snippet or a page-scoped inline block that survives REST serialization.
- When pages already exist, update by slug rather than creating duplicates. If slug lookup fails, create the page and then re-fetch/update by ID.

## Theme/plugin pitfalls found in portfolio landing pages
- TOC plugins can inject a visible table of contents into hero sections and ruin above-the-fold UX. For landing pages, page-scope suppress common TOC containers such as `.lwptoc`, `.ez-toc-container`, `#ez-toc-container`, `.toc`, `.table-of-contents`, and `.wp-block-rank-math-toc-block` unless a TOC is deliberately part of the design.
- Some themes constrain REST content inside narrow block containers. Page-scope full-width CSS may need to target `.entry-content`, `.site-main`, `.content-area`, `.wp-site-blocks`, `.is-layout-constrained`, `.alignwide`, and `.alignfull`; for stubborn cases set the landing wrapper to `width:100vw`, `max-width:none`, and center with `margin-left:calc(50% - 50vw)` / `margin-right:calc(50% - 50vw)`.
- Floating chat widgets, cookie revisit buttons, back-to-top widgets, and iframe chat launchers can overlap premium heroes. Suppress page-scoped selectors when they distract from the CTA: `iframe[title*='Chat']`, `iframe[src*='tawk']`, `[class*='chat']`, `[id*='chat']`, `.cky-btn-revisit-wrapper`, `.generate-back-to-top`, and site-specific concierge roots.
- Internal-link discovery from sitemaps should be recursive: fetch sitemap indexes, parse child sitemaps, then collect real post/page URLs. Avoid using sitemap XML URLs themselves as public internal links.

## Live QA checklist before reporting done
- HTTP 200 public URL.
- Canonical points to the final SEO page.
- No `noindex` in robots meta or headers.
- Exactly one source/live H1 unless the theme requires a documented exception, then repair.
- App CTA links present and point to the requested subdomain.
- JSON-LD parses enough to find expected schema types.
- Internal links resolve to real pages, not sitemap XML files.
- Browser QA: above-the-fold page is visible, premium/readable, full-width as designed, no hero clipping, no horizontal overflow, no intrusive TOC/cookie/chat/back-to-top overlay.
- Cache-bust QA URLs with a query string after updates.

## Reporting standard
Report only after publishing and verification. Include the live URLs, app targets, what was built, critical fixes applied during QA, and any blockers. Do not over-explain the implementation when the user asked to proceed aggressively.