---
name: wordpress-eeat-remediation-via-rest
description: Upgrade WordPress E-E-A-T / trust signals safely via REST API when Cloudflare blocks wp-admin. Covers author pages, editorial policy, disclosure, methodology, trust blocks, redirects, and careful cleanup of unsupported claims.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [wordpress, eeat, trust, rest-api, cloudflare, yoast, author-pages, disclosure]
    triggers: [fix eeat, improve trust signals, editorial policy, author page, affiliate disclosure, unsupported claims]
---

# WordPress E-E-A-T Remediation via REST

Use this when a WordPress site needs trust/E-E-A-T upgrades but wp-admin is blocked by Cloudflare and REST access works.

## Core principles
1. Do not fabricate credentials, certifications, income proof, expert reviewers, company registration, or physical address details.
2. Prefer founder-led honesty over inflated authority claims.
3. Back up every page/user object before editing.
4. Use POST + `X-HTTP-Method-Override: PUT` for updates.
5. Verify live URLs after every change.
6. Treat trust signals as ranking infrastructure, not decorative legal pages.
7. When planning SEO improvements, compare trust assets against the real SERP competitors, not just the site's current structure.
## Best workflow

### 1. Discover trust assets and author objects
Check for:
- editorial policy page
- review methodology page
- about page
- dedicated author page
- contact page
- affiliate disclosure page
- WordPress user profiles (`/wp-json/wp/v2/users/{id}?context=edit`)
- duplicate thin policy pages that should redirect to a canonical page

Useful endpoints:
- `/wp-json/wp/v2/pages?search=editorial&context=edit`
- `/wp-json/wp/v2/pages?search=about&context=edit`
- `/wp-json/wp/v2/pages?search=contact&context=edit`
- `/wp-json/wp/v2/pages?search=methodology&context=edit`
- `/wp-json/wp/v2/users?context=edit`

### 2. Back up before editing
Save raw JSON for every page/post/user you will touch.
Recommended minimum:
- page JSON backups under `/tmp/...json`
- homepage raw content backup if editing homepage
- note duplicate URLs before redirecting them

### 3. Strengthen core trust pages
Create or upgrade these pages before or alongside archive-wide SEO upgrades so internal trust links point to strong assets, not thin placeholders:

#### Editorial policy
Should include:
- what the site publishes
- research / verification standards
- review methodology summary
- updates and freshness policy
- corrections policy
- AI usage policy link
- disclosure / conflict-of-interest language
- explicit statement if the site is founder-led rather than a large editorial team

#### Author page
Should include only verifiable info:
- author role
- editorial focus / research areas
- transparency statement
- editorial contact
- links to policy / methodology / disclosure pages

#### About page
Fix common trust problems:
- remove fake “team of experts” language if not true
- replace with honest founder-led publication identity
- link to editorial policy, disclosure, contact, author page

#### Affiliate disclosure
Replace generator-style legal filler with:
- what affiliate links are
- what they do not mean
- how recommendations are evaluated
- no-guarantees language
- third-party responsibility limits
- correction/contact path

#### Review methodology
Create a strong canonical trust asset containing:
- what gets evaluated
- what the site does not claim
- how review pages are built
- related trust pages
- corrections path

### 4. Update user profiles too
Important finding: WordPress REST can update user descriptions and URLs directly.
Use `/wp-json/wp/v2/users/{id}` to improve:
- `description`
- `url`

This helps author archive trust signals and can improve how themes/SEO plugins surface author data.

### 5. Fix author-link routing
Check live posts for the byline author URL.
If author links point to the homepage or a weak profile, update the relevant user/page setup so post author links resolve to the real author page.
Verify on multiple live posts.

### 6. Add trust blocks to commercial pages
Reusable low-risk pattern:
- prepend an “Editorial review” block linking to editorial policy, methodology, and disclosure
- prepend an “Evidence note” block on stat-heavy pages clarifying that examples / ranges / scenarios are illustrative unless directly cited
- add trust links near high-intent CTAs, comparison tables, and monetization claims

Good targets:
- affiliate reviews
- monetization pages
- comparison pages
- alternatives pages
- use-case pages
- start-here commercial guides
- stat-heavy legacy posts

Enterprise rule:
If a page is supposed to rank for a money term, its trust layer should be intentionally visible and internally linked, not buried in the footer.

### 6b. Trust copy must still feel premium and human
When trust remediation overlaps with content rewriting, also load `wordpress-sota-seo-content-system`.
For compact trust UI modules and proof-element patterns, also load `wordpress-trust-blocks-and-proof-elements`.

Required standard:
- trust blocks should be elegant, restrained, and visually clean
- copy must sound human and specific, not legal-generator sludge
- use compact panels, warnings, checklists, or methodology notes only where they improve confidence
- preserve strong original content instead of replacing it with generic compliance filler
- if a page needs a premium visual HTML component, keep it simple enough to survive the theme without distortion

### 7. Clean risky unsupported claims
Look for:
- dramatic percentages with no citations
- “success rate” claims
- invented revenue numbers
- hype phrases like `100,000X better`
- fake team/expert language

Preferred remediation order:
1. Remove obviously fabricated-sounding claims entirely
2. Rephrase to general operational guidance
3. Add an evidence-note block when a full citation cleanup is too large for one pass

### 8. Consolidate duplicate trust pages with redirects
If multiple thin editorial/methodology pages exist, keep one canonical version and redirect the others.
Useful finding: Yoast redirects can be created through REST:
- POST `/wp-json/yoast/v1/redirects`

Example uses:
- duplicate editorial policy pages -> canonical editorial policy
- short alias like `/review-methodology/` -> full canonical methodology URL
- root-style convenience paths when file-level access is unavailable

### 9. File-level workaround via REST uploads + redirects
If you need a root-like asset such as `llms.txt` but lack filesystem access:
1. upload text file via `/wp-json/wp/v2/media`
2. create a Yoast redirect from `/llms.txt` to the uploaded media URL
3. verify it returns `200 text/plain`

### 10. Verification checklist
Always verify live, not just via REST response.

Check:
- trust pages return 200
- duplicate URLs redirect correctly
- author links on live posts point to the correct author page
- `Updated on` and `dateModified` already present or still intact
- editorial review blocks visible on target pages
- evidence notes visible on stat-heavy pages
- removed hype claims are truly gone from live HTML

## Practical content rules learned
- Founder-led honesty is stronger than fake authority inflation.
- If external proof does not exist, say less and make governance clearer.
- A clear corrections path is a real trust improvement.
- An evidence-note block is a safe interim mitigation for legacy archives full of unsupported stats.
- For trust pages, custom `<!-- wp:html -->` sections are reliable and avoid layout corruption.

## Output contract
Report:
- exactly which URLs were changed
- which claims/blocks were added or removed
- what was verified live
- which remaining gaps require real user-supplied evidence or broader archive work
