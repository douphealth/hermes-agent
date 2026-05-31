# WordPress Freemium App Funnel Architecture

Use this pattern when a WordPress content site has a freemium calculator/quiz/planner/app hosted on a subdomain.

## Core architecture

Use both assets:

1. **Main-domain SEO landing page** — ranks, explains, earns internal links, builds trust.
2. **Subdomain app** — converts through the quiz/planner/app UX, free result, paid upgrade, email capture, and follow-up sequence.

Default flow:

```text
Organic query → WordPress SEO landing page → subdomain app → free result → paid upgrade → email nurture → affiliate/digital-product upsell
```

High-intent exceptions can link directly from an article CTA to the subdomain app, but the main-domain landing page remains the primary SEO asset.

## Why not only the subdomain?

- Main domain usually has stronger topical authority, sitemap history, internal links, trust pages, and WordPress SEO/schema controls.
- Subdomains can rank, but should not be the only rankable asset for a commercial app funnel.
- WordPress articles can route authority into the landing page with contextual internal links.
- The app subdomain can remain fast, clean, focused, and free from WP/plugin conflicts.

## Landing page requirements

Each app needs a non-thin SEO landing page on the main domain with:

- one keyword-focused H1
- answer-first intro explaining the outcome
- clear free vs paid value explanation
- who it is for / who it is not for
- screenshots or mockups when available
- 3–5 benefit sections
- trust/disclaimer block where relevant
- visible FAQ section
- Article/WebPage/Breadcrumb schema, plus FAQ schema only if FAQs are visible
- contextual internal links from related posts and pillar pages
- strong CTA button to the subdomain app
- UTM-tagged CTA URL

## CTA placement system

Use four CTA types:

1. **Homepage hero CTA** — primary button to app or SEO landing page.
2. **In-article problem CTA** — after the article defines the problem.
3. **Mid-article decision CTA** — after options/criteria are explained.
4. **End-of-article next-step CTA** — final conversion prompt.

Default linking:

```text
Informational article → SEO landing page → app
Problem-aware/high-intent article → direct app CTA may be added
Homepage/nav/footer/sidebar → SEO landing page or app depending on copy and intent
```

## Tracking

Append UTM parameters to app CTAs:

```text
?utm_source=<site>&utm_medium=<homepage|article|landing_page>&utm_campaign=<app_name>&utm_content=<slug_or_block>
```

Capture these in the app when possible:

- source site
- source URL
- CTA position/content
- user goal/problem
- email
- free vs paid status
- recommended product/category

## User portfolio app map

- AMFS: SEO page `/free-affiliate-marketing-plan/`; app `https://start-here.affiliatemarketingforsuccess.com`
- FrenchyFab: SEO page `/french-bulldog-care-plan/`; app `https://care-plan.frenchyfab.com`
- GearUpToFit fitness: SEO page `/free-fitness-plan/`; app `https://fitness-plan.gearuptofit.com/`
- GearUpToFit shoes: SEO page `/shoe-finder/`; app `https://shoe-match.gearuptofit.com/`
- MysticalDigits: SEO page `/life-path-calculator/`; app `https://life-path.mysticaldigits.com`
- PlantasticHaven: SEO page `/plant-care-plan/`; app `https://procare.plantastichaven.com`
- MiceGoneGuide: SEO page `/mouse-elimination-plan/`; app `https://elimination.micegoneguide.com`
- GearUpToGrow: SEO page `/growth-plan/`; app `https://grow-plan.gearuptogrow.com`

## Pitfalls

- Do not make a thin landing page that is only a button; it will not earn trust or rank well.
- Do not rely solely on the subdomain for SEO.
- Do not send every article directly to the app; consolidate SEO equity through the main-domain landing page unless intent is already high.
- Do not push paid upgrade before the free result demonstrates value.
- Do not forget UTM/source capture; the apps need to identify which pages and CTAs generate paid users.
