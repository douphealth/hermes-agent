# WordPress article quality rescue: duplicate titles, fake links, and keyword-stuffing cleanup

Use this reference when a WordPress SEO/content rewrite accidentally publishes machine-like NeuronWriter/SEO padding, duplicate title blocks, or internal links that are technically present but not useful to readers.

## Failure signatures from a real cleanup

Hard-fail phrases/patterns:

- `use this as an audit label, editorial requirement, or measurement checkpoint`
- `include this concept in your operating checklist`
- Long blocks of repeated `<strong>keyword:</strong> generic sentence` entries
- Mechanical headings such as `Become An Affiliate Marketer`, `Affiliate Marketer`, `Beginner`, `Popular Types of Content Marketing` followed by repeated templated text
- Sections named like `Implementation Notes`, `Tips`, or `Popular Types...` that only exist to stuff SEO terms
- A large body H2 immediately under the theme H1 that repeats/paraphrases the SEO title
- Related-links cards added at the bottom while the actual article paragraphs contain no contextual internal links

## Rescue workflow

1. Back up the current post via XML-RPC/REST before editing.
2. Load the stored post body and locate the bad section by exact phrase, not by screenshot alone.
3. Remove the entire generated-padding section, including parent headings that introduced it.
4. Replace with a reader-facing section that explains decisions, examples, or a checklist.
5. Add contextual internal links inside natural paragraphs and bullets where the linked concept is discussed. A related-resources grid is only supplemental.
6. Remove body `<h1>` tags and also remove or downshift duplicate visual hero titles; use a short `Quick strategy brief:` paragraph instead of another oversized title.
7. Publish by XML-RPC when rich HTML/CSS must be preserved.
8. Purge Cloudflare exact URLs and WordPress/page-cache plugin caches.
9. Verify three surfaces:
   - Stored post body: no body H1, no hard-fail phrases, internal links present.
   - Raw public HTML: one total H1, no visible CSS/schema leaks after stripping style/script/svg.
   - Browser DOM/innerText: bad phrases absent, duplicate title absent, article internal links visible, no horizontal overflow.

## Minimal verification probes

Stored/public text probes should assert all of the following:

- `'<h1' not in stored_body.lower()`
- `use this as an audit label` absent
- `include this concept in your operating checklist` absent
- old bad section headings absent
- replacement section heading present
- `href="https://affiliatemarketingforsuccess.com/` count meets target

Browser probe should return:

- `document.querySelectorAll('h1').length === 1`
- `article.querySelectorAll('h1').length === 0`
- `document.body.innerText.includes(badPhrase) === false`
- `article.querySelectorAll('a[href^="https://affiliatemarketingforsuccess.com/"]').length` high enough
- `document.documentElement.scrollWidth - document.documentElement.clientWidth === 0`

## Replacement-section examples

For affiliate strategy padding, replace with a section like `Execution Notes: Build Authority Without Keyword Stuffing` and cover:

- beginner niche validation
- SEO/topical-authority support pages
- affiliate program comparison
- trust and compliance mistakes

For content marketing padding, replace with `Content Marketing Types: Where Each Format Fits` and cover:

- educational content
- comparison/decision content
- distribution content
- authority-building content
- keep/refresh/consolidate/create decisions

## Reporting standard

Keep the report short and evidence-led: URL, removed block, replacement section, H1 count, bad phrase absent, contextual internal-link counts, cache purge status, and backup path.