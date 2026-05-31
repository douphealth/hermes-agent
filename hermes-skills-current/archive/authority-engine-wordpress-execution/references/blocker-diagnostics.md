# WordPress SEO Blocker Diagnostics

Use this when REST writes succeed but live SEO output is inconsistent.

## Check 1: Body vs head split-brain
Symptoms:
- H1/body updated
- `<title>` / meta description still stale
- og:title may or may not sync

Action:
- verify public head separately
- identify plugin namespace/routes if exposed
- report plugin-layer blocker explicitly

## Check 2: Plain URL vs cache-busted divergence
Symptoms:
- `?v=timestamp` shows fixed output
- plain URL still broken or stale

Action:
- treat cache/optimization layer as the bug
- inspect active acceleration/minification plugins
- do not call the issue fixed until plain URL is correct too

## Check 3: Duplicate H1 caused by theme + body hero
Symptoms:
- theme entry title renders H1
- custom HTML hero also contains H1

Action:
- preserve design
- demote decorative hero H1 to H2
- re-verify H1 count live

## Check 4: Duplicate trust assets with no redirect support
Symptoms:
- multiple editorial/disclosure/methodology pages
- REST can edit pages but not create live redirects

Action:
- keep one canonical trust asset
- convert weaker pages into support pages pointing to the canonical asset
- normalize internal links toward the canonical asset

## Check 5: Auto-formatting breaks custom layouts
Symptoms:
- REST write succeeds but layout gains `<p>` / `<br>` pollution

Action:
- wrap custom HTML/CSS/JS in `<!-- wp:html -->`
- re-verify visible rendering live
