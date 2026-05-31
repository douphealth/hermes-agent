---
name: redesign
description: Upgrades existing websites and apps to premium quality. Audits current design, identifies generic AI patterns, and applies high-end design standards without breaking functionality. Works with any CSS framework or vanilla CSS.
version: 1.0.0
author: Adapted from taste-skill by Leonxlnx for Hermes Agent
---

# Redesign Skill

## How This Works

When redesigning an existing project, follow this sequence:

1. **Scan** — Read the codebase or page. Identify the framework, styling method (Tailwind, vanilla CSS, styled-components, etc.), and current design patterns.
2. **Diagnose** — Run through the audit below. List every generic pattern, weak point, and missing state you find.
3. **Fix** — Apply targeted upgrades working with the existing stack. Do not rewrite from scratch. Improve what's there.

If the redesign target is WordPress page/post content rather than a standalone frontend, also load `wordpress-sota-seo-content-system`.
That skill adds the rewrite quality bar for:
- premium human-style copy
- answer-first content structure
- elegant HTML modules inside WordPress
- schema/internal-link decisions
- rewrite safety and verification

## Design Audit

### Typography

Check for these problems and fix them:

- **Browser default fonts or Inter everywhere.** Replace with a font that has character. Good options: `Geist`, `Outfit`, `Cabinet Grotesk`, `Satoshi`. For editorial/creative projects, pair a serif header with a sans-serif body.
- **Headlines lack presence.** Increase size for display text, tighten letter-spacing, reduce line-height. Headlines should feel heavy and intentional.
- **Body text too wide.** Limit paragraph width to roughly 65 characters. Increase line-height for readability.
- **Only Regular (400) and Bold (700) weights used.** Introduce Medium (500) and SemiBold (600) for more subtle hierarchy.
- **Numbers in proportional font.** Use a monospace font or enable tabular figures (`font-variant-numeric: tabular-nums`) for data-heavy interfaces.
- **Missing letter-spacing adjustments.** Use negative tracking for large headers, positive tracking for small caps or labels.
- **All-caps subheaders everywhere.** Try lowercase italics, sentence case, or small-caps instead.
- **Orphaned words.** Single words sitting alone on the last line. Fix with `text-wrap: balance` or `text-wrap: pretty`.

### Color and Surfaces

- **Pure `#000000` background.** Replace with off-black, dark charcoal, or tinted dark (`#0a0a0a`, `#121212`, or a dark navy).
- **Oversaturated accent colors.** Keep saturation below 80%. Desaturate accents so they blend with neutrals instead of screaming.
- **More than one accent color.** Pick one. Remove the rest. Consistency beats variety.
- **Mixing warm and cool grays.** Stick to one gray family. Tint all grays with a consistent hue (warm or cool, not both).
- **Purple/blue "AI gradient" aesthetic.** This is the most common AI design fingerprint. Replace with neutral bases and a single, considered accent.
- **Generic `box-shadow`.** Tint shadows to match the background hue. Use colored shadows (e.g., dark blue shadow on a blue background) instead of pure black at low opacity.
- **Flat design with zero texture.** Add subtle noise, grain, or micro-patterns to backgrounds. Pure flat vectors feel sterile.
- **Perfectly even gradients.** Break the uniformity with radial gradients, noise overlays, or mesh gradients instead of standard linear 45-degree fades.
- **Inconsistent lighting direction.** Audit all shadows to ensure they suggest a single, consistent light source.
- **Random dark sections in a light mode page (or vice versa).** A single dark-background section breaking an otherwise light page looks like a copy-paste accident. Either commit to a full dark mode or keep a consistent background tone throughout.
- **Empty, flat sections with no visual depth.** Sections that are just text on a plain background feel unfinished. Add high-quality background imagery (blurred, overlaid, or masked), subtle patterns, or ambient gradients. Use reliable placeholder sources like `https://picsum.photos/seed/{name}/1920/1080` when real assets are not available.

### Layout

- **WordPress landing pages trapped in the theme content column.** For premium app/SaaS landing pages built inside `<!-- wp:html -->`, use a scoped full-bleed wrapper (`width:100vw; margin-left:calc(50% - 50vw); overflow-x:clip`) plus a wider inner container and responsive hero breakpoints. See `references/wordpress-full-bleed-responsive-landing-pages.md`.
   - **⚠️ Elementor body flex blank-after-animation.** When Elementor sets `body { display: flex; flex-direction: column; min-height: 577px }` (common on Elementor sites) with a `siteReveal` fade-in animation, the page can go blank after the animation ends because the flex body doesn't contain full-bleed content. See `references/wp-elementor-body-flex-blank-animation-fix.md`.
- **WordPress commercial posts published via REST can look fine in source but break visually on mobile.** Do not use `<style>`/`@media` blocks in REST-written post bodies unless XML-RPC or another preservation path is verified; REST may strip the tag and leak raw CSS as visible text. Build REST-safe inline-styled modules, avoid wide tables, stack product cards at 320px, keep only one real `<h1>`, and run rendered 320px/390px overflow + skinny-text checks before claiming SOTA quality. See `references/wordpress-rest-safe-mobile-commercial-posts.md`.
- **WordPress public posts can be clean in the database but still leak/break in public rendering.** When the user reports raw HTML/CSS leakage, duplicated article bodies, exposed implementation notes, or broken mobile fit, treat public rendered output as the source of truth. Strip malformed Gutenberg block comments if needed, republish clean HTML, add site-level mobile rescue CSS via Customizer/Additional CSS with a public marker, purge plugin/CDN cache, and verify visible text plus 320px/390px layout before claiming fixed. See `references/wordpress-public-post-leakage-mobile-rescue.md`.
- **Everything centered and symmetrical.** Break symmetry with offset margins, mixed aspect ratios, or left-aligned headers over centered content.
- **Three equal card columns as feature row.** This is the most generic AI layout. Replace with a 2-column zig-zag, asymmetric grid, horizontal scroll, or masonry layout.
- **Using `height: 100vh` for full-screen sections.** Replace with `min-height: 100dvh` to prevent layout jumping on mobile browsers (iOS Safari viewport bug).
- **Complex flexbox percentage math.** Replace with CSS Grid for reliable multi-column structures.
- **No max-width container.** Add a container constraint (around 1200-1440px) with auto margins so content doesn't stretch edge-to-edge on wide screens.
- **Cards of equal height forced by flexbox.** Allow variable heights or use masonry when content varies in length.
- **Uniform border-radius on everything.** Vary the radius: tighter on inner elements, softer on containers.
- **No overlap or depth.** Elements sit flat next to each other. Use negative margins to create layering and visual depth.
- **Symmetrical vertical padding.** Top and bottom padding are always identical. Adjust optically — bottom padding often needs to be slightly larger.
- **Dashboard always has a left sidebar.** Try top navigation, a floating command menu, or a collapsible panel instead.
- **Missing whitespace.** Double the spacing. Let the design breathe. Dense layouts work for data dashboards, not for marketing pages.
- **Buttons not bottom-aligned in card groups.** When cards have different content lengths, CTAs end up at random heights. Pin buttons to the bottom of each card so they form a clean horizontal line regardless of content above.
- **Feature lists starting at different vertical positions.** In pricing tables or comparison cards, the list of features should start at the same Y position across all columns. Use consistent spacing above the list or fixed-height title/price blocks.
- **Inconsistent vertical rhythm in side-by-side elements.** When placing cards, columns, or panels next to each other, align shared elements (titles, descriptions, prices, buttons) across all items. Misaligned baselines make the layout look broken.
- **Mathematical alignment that looks optically wrong.** Centering by the math doesn't always look centered to the eye. Icons next to text, play buttons in circles, or text in buttons often need 1-2px optical adjustments to feel right.

### Interactivity and States

- **No hover states on buttons.** Add background shift, slight scale, or translate on hover.
- **No active/pressed feedback.** Add a subtle `scale(0.98)` or `translateY(1px)` on press to simulate a physical click.
- **Instant transitions with zero duration.** Add smooth transitions (200-300ms) to all interactive elements.
- **Missing focus ring.** Ensure visible focus indicators for keyboard navigation. This is an accessibility requirement, not optional.
- **No loading states.** Replace generic circular spinners with skeleton loaders that match the layout shape.
- **No empty states.** An empty dashboard showing nothing is a missed opportunity. Design a composed "getting started" view.
- **No error states.** Add clear, inline error messages for forms. Do not use `window.alert()`.
- **Dead links.** Buttons that link to `#`. Either link to real destinations or visually disable them.
- **No indication of current page in navigation.** Style the active nav link differently so users know where they are.
- **Scroll jumping.** Anchor clicks jump instantly. Add `scroll-behavior: smooth`.
- **Animations using `top`, `left`, `width`, `height`.** Switch to `transform` and `opacity` for GPU-accelerated, smooth animation.

### Content

- **Generic names like "John Doe" or "Jane Smith".** Use diverse, realistic-sounding names.
- **Fake round numbers like `99.99%`, `50%`, `$100.00`.** Use organic, messy data: `47.2%`, `$99.00`, `+1 (312) 847-1928`.
- **Placeholder company names like "Acme Corp", "Nexus", "SmartFlow".** Invent contextual, believable brand names.
- **AI copywriting cliches.** Never use "Elevate", "Seamless", "Unleash", "Next-Gen", "Game-changer", "Delve", "Tapestry", or "In the world of...". Write plain, specific language.
- **Exclamation marks in success messages.** Remove them. Be confident, not loud.
- **"Oops!" error messages.** Be direct: "Connection failed. Please try again."
- **Passive voice.** Use active voice: "We couldn't save your changes" instead of "Mistakes were made."
- **All blog post dates identical.** Randomize dates to appear real.
- **Same avatar image for multiple users.** Use unique assets for every distinct person.
- **Lorem Ipsum.** Never use placeholder latin text. Write real draft copy.
- **Title Case On Every Header.** Use sentence case instead.

### Component Patterns

- **Generic card look (border + shadow + white background).** Remove the border, or use only background color, or use only spacing. Cards should exist only when elevation communicates hierarchy.
- **Always one filled button + one ghost button.** Add text links or tertiary styles to reduce visual noise.
- **Pill-shaped "New" and "Beta" badges.** Try square badges, flags, or plain text labels.
- **Accordion FAQ sections.** Use a side-by-side list, searchable help, or inline progressive disclosure.
- **3-card carousel testimonials with dots.** Replace with a masonry wall, embedded social posts, or a single rotating quote.
- **Pricing table with 3 towers.** Highlight the recommended tier with color and emphasis, not just extra height.
- **Modals for everything.** Use inline editing, slide-over panels, or expandable sections instead of popups for simple actions.
- **Avatar circles exclusively.** Try squircles or rounded squares for a less generic look.
- **Light/dark toggle always a sun/moon switch.** Use a dropdown, system preference detection, or integrate it into settings.
- **Footer link farm with 4 columns.** Simplify. Focus on main navigational paths and legally required links.

### Iconography

- **Lucide or Feather icons exclusively.** These are the "default" AI icon choice. Use Phosphor, Heroicons, or a custom set for differentiation.
- **Rocketship for "Launch", shield for "Security".** Replace cliche metaphors with less obvious icons (bolt, fingerprint, spark, vault).
- **Inconsistent stroke widths across icons.** Audit all icons and standardize to one stroke weight.
- **Missing favicon.** Always include a branded favicon.
- **Stock "diverse team" photos.** Use real team photos, candid shots, or a consistent illustration style instead of uncanny stock imagery.

### Code Quality

- **Div soup.** Use semantic HTML: `<nav>`, `<main>`, `<article>`, `<aside>`, `<section>`.
- **Inline styles mixed with CSS classes.** Move all styling to the project's styling system.
- **Hardcoded pixel widths.** Use relative units (`%`, `rem`, `em`, `max-width`) for flexible layouts.
- **Missing alt text on images.** Describe image content for screen readers. Never leave `alt=""` or `alt="image"` on meaningful images.
- **Arbitrary z-index values like `9999`.** Establish a clean z-index scale in the theme/variables.
- **Commented-out dead code.** Remove all debug artifacts before shipping.
- **Import hallucinations.** Check that every import actually exists in the project dependencies.
- **Missing meta tags.** Add proper `<title>`, `description`, `og:image`, and social sharing meta tags.

### Strategic Omissions (What AI Typically Forgets)

- **No legal links.** Add privacy policy and terms of service links in the footer.
- **No "back" navigation.** Dead ends in user flows. Every page needs a way back.
- **No custom 404 page.** Design a helpful, branded "page not found" experience.
- **No form validation.** Add client-side validation for emails, required fields, and format checks.
- **No "skip to content" link.** Essential for keyboard users. Add a hidden skip-link.
- **No cookie consent.** If required by jurisdiction, add a compliant consent banner.

## Upgrade Techniques

### Typography Upgrades
- **Variable font animation.** Interpolate weight or width on scroll or hover for text that feels alive.
- **Outlined-to-fill transitions.** Text starts as a stroke outline and fills with color on scroll entry or interaction.
- **Text mask reveals.** Large typography acting as a window to video or animated imagery behind it.

### Layout Upgrades
- **Broken grid / asymmetry.** Elements that deliberately ignore column structure — overlapping, bleeding off-screen, or offset with calculated randomness.
- **Whitespace maximization.** Aggressive use of negative space to force focus on a single element.
- **Parallax card stacks.** Sections that stick and physically stack over each other during scroll.
- **Split-screen scroll.** Two halves of the screen sliding in opposite directions.

### Motion Upgrades
- **Smooth scroll with inertia.** Decouple scrolling from browser defaults for a heavier, cinematic feel.
- **Staggered entry.** Elements cascade in with slight delays, combining Y-axis translation with opacity fade.
- **Spring physics.** Replace linear easing with spring-based motion for a natural, weighty feel on all interactive elements.
- **Scroll-driven reveals.** Content entering through expanding masks, wipes, or draw-on SVG paths tied to scroll progress.

### Surface Upgrades
- **True glassmorphism.** Go beyond `backdrop-filter: blur`. Add a 1px inner border and a subtle inner shadow to simulate edge refraction.
- **Spotlight borders.** Card borders that illuminate dynamically under the cursor.
- **Grain and noise overlays.** A fixed, pointer-events-none overlay with subtle noise to break digital flatness.
- **Colored, tinted shadows.** Shadows that carry the hue of the background rather than using generic black.

## Fix Priority

Apply changes in this order for maximum visual impact with minimum risk:

1. **Font swap** — biggest instant improvement, lowest risk
2. **Color palette cleanup** — remove clashing or oversaturated colors
3. **Hover and active states** — makes the interface feel alive
4. **Layout and spacing** — proper grid, max-width, consistent padding
5. **Replace generic components** — swap cliche patterns for modern alternatives
6. **Add loading, empty, and error states** — makes it feel finished
7. **Polish typography scale and spacing** — the premium final touch

## Rules

- Work with the existing tech stack. Do not migrate frameworks or styling libraries.
- Do not break existing functionality. Test after every change.
- Before importing any new library, check the project's dependency file first.
- If the project uses Tailwind, check the version (v3 vs v4) before modifying config.
- If the project has no framework, use vanilla CSS.
- Keep changes reviewable and focused. Small, targeted improvements over big rewrites.


## WordPress Visual Diagnosis via Browser

When a WordPress site (especially Elementor) looks distorted and you don't have WP admin access, use browser console (`browser_console`) to systematically diagnose the layout. This avoids the Cloudflare block that hits `wp-login.php`.

### Diagnosis Sequence

1. **Navigate to the live page** → `browser_navigate(url)`
2. **Check top-level structure** → Inspect `document.body` children, especially `.elementor-location-header`, `.elementor-location-single`, `.elementor-location-single > div`
3. **Find the post content widget** → Look for `.elementor-widget-theme-post-content` — this is where the actual article HTML lives
4. **Check the theme-published article wrapper** → Many sites use a custom class (e.g., `.gutf-article`, `.entry-content`, `.post-content`). Check its `getComputedStyle` for width, maxWidth, padding, margin
5. **Check for overflow** → `document.documentElement.scrollWidth - document.documentElement.clientWidth` — nonzero means horizontal scroll
6. **Check responsive breakpoints** → The existing `@media (max-width: 767px)` rules may be incomplete. Common misses: tables without `overflow-x: auto`, flex rows without `flex-wrap: wrap`, fixed-width elements
7. **Audit all inline `<style>` blocks** → `document.querySelectorAll('style')` — the page may inject dozens of fragmented inline CSS blocks. Look for the block that styles the main content area
8. **Check body layout mode** → Many Elementor themes set `body { display: flex }`, which can clip full-bleed content or break scroll. `getComputedStyle(document.body)`

### Common Elementor Layout Failures (Desktop)

| Issue | Detection | Fix |
|-------|-----------|-----|
| Container too wide | `.e-con` or `.elementor-widget-container` width > 900px | Add `max-width: 880px` to `.gutf-article` or constrain the Elementor container |
| Body flex breaks content | `body { display: flex }` + `overflow-x: clip` | Change body to `display: block` or ensure children are 100% width |
| Post content widget full-width no padding | `.elementor-widget-theme-post-content` width = 1140px | Add padding to the widget, or constrain children |
| Only 1 section in elementor-location-single | Means all content is in a single container — likely Elementor template is just wrapping raw post HTML | CSS overrides needed, not structural changes |

### Common Elementor Layout Failures (Mobile)

| Issue | Detection | Fix |
|-------|-----------|-----|
| Tables overflow | Table width > viewport | `table { display: block; overflow-x: auto; white-space: nowrap }` |
| Product boxes collapse | Flex row children don't wrap | Add `flex-wrap: wrap` to `.product-box-inner` |
| Fixed-width content breaks | Any element with explicit `width: <fixed px>` > viewport | Replace with `max-width: 100%` or responsive units |
| Images stretch | `img { width: 100%; height: auto }` missing | Add these styles for all `.gutf-article img` |
| Readability on mobile | Body text 18px+ with no responsive adjustment | Use `clamp(16px, 2vw, 18px)` for body text |
| Article hero crushed into a skinny column | A semantic post `<header>` or hero wrapper inherits global theme/Elementor `header { display:flex }`, fixed child widths, floats, or transforms | Inject a scoped post-level rescue: force the article hero `display:block`, children `position:static; float:none; width:100%; min-width:0`, and stack pills/badges. See `references/wordpress-post-mobile-rescue-css.md` |

### Cloudflare Considerations

- `wp-login.php` and `wp-admin/` are typically behind Cloudflare bot protection
- `wp-json/wp/v2/` (REST API) is often accessible without auth for reads
- If you need auth, you must either: (a) add credentials to the browser session, (b) use a residential proxy, or (c) find the application password approach via the REST API
- For CSS-only fixes, injecting via `wp-admin/themes.php?page=...` isn't possible through automated browser
- The site may already have a "Custom CSS" or "Additional CSS" field populated — check for `#wp-custom-css` or `style[class*="custom-css"]` in the head

### Existing Hotfix Detection

Before making changes, check whether there's already a mobile-distortion hotfix on the page. After making changes on WordPress, do not trust the stored page body alone: add a unique marker to the hotfix, confirm it exists in stored XML-RPC/REST content, then confirm the same marker exists in public apex/origin raw HTML after cache purge before browser QA. If the marker is absent publicly, keep clearing Cloudflare/plugin cache instead of claiming the visual fix is live.

```javascript
// Check for existing hotfix CSS
document.querySelector('style[id*="mobile-distortion"]')?.innerHTML
document.querySelector('style[id*="hotfix"]')?.innerHTML
document.querySelector('style[id*="mobile"]')?.innerHTML
```

If one exists but the issue persists, the hotfix may be:
- Too narrow (only targets E-E-A-T sections, not main content)
- Missing `@media` breakpoints
- Using `!important` on wrong selectors

### Quick Verification

After any CSS change, re-verify with:

```javascript
// No overflow?
document.documentElement.scrollWidth - document.documentElement.clientWidth

// Content readable width?
document.querySelector('.gutf-article, .entry-content')?.getBoundingClientRect()

// For premium WordPress commercial/review posts, also run the iframe-based 320px/390px mobile probe in
// references/wordpress-rest-safe-mobile-commercial-posts.md to catch skinny product cards, visible CSS leaks,
// injected figures/blank gaps, and table/card overflow.
```

## Consolidated Reference Index

The following formerly separate narrow skills have been absorbed into this umbrella. Load the listed reference file only when that specific provider, failure mode, or workflow detail is needed.

- `premium-wordpress-html-blocks` → `references/premium-wordpress-html-blocks.md`
- `wordpress-full-bleed-responsive-landing-pages` → `references/wordpress-full-bleed-responsive-landing-pages.md` — scoped full-bleed WordPress HTML block pattern, responsive hero breakpoints, and browser overflow verification for landing pages that need to cover the viewport better.
- `gearuptofit-twentyten-landing-pages` → `references/gearuptofit-twentyten-landing-pages.md` — site-specific Twenty Ten child theme rescue pattern: REST-created page ID CSS, sidebar hiding, off-canvas theme title, and Frase widget obstruction fix.
- `taste-design` → `references/taste-design.md`
- `wp-elementor-body-flex-blank-animation-fix` → `references/wp-elementor-body-flex-blank-animation-fix.md` — diagnosing blank-page-after-animation when Elementor sets `body { display: flex; min-height: 577px }` combined with body entry animations. Fix pattern and prevention checklist for full-bleed WordPress pages.
- `wordpress-css-injection-bypass-techniques` → `references/wordpress-css-injection-bypass-techniques.md` — injection fallback priority when REST API write fails and wp-admin is behind Cloudflare. XML-RPC as primary bypass, plus wp-custom-css, plugin hooks, and direct file edit options. Cache pitfalls with PhastPress and Cloudflare.
- `wordpress-post-mobile-rescue-css` → `references/wordpress-post-mobile-rescue-css.md` — scoped hotfix pattern for WordPress/Elementor posts whose internal hero/header blocks are crushed on mobile by global theme flex/floats; includes iframe DOM verification and cache-bypass criteria.
- `wordpress-rest-safe-mobile-commercial-posts` → `references/wordpress-rest-safe-mobile-commercial-posts.md` — REST-safe inline-styled commercial/review post pattern, 320px/390px iframe QA probe, raw CSS leak prevention, skinny-card detection, and WordPress theme/plugin heading-image injection mitigation.
- `wordpress-public-post-leakage-mobile-rescue` → `references/wordpress-public-post-leakage-mobile-rescue.md` — recovery workflow for WordPress posts whose public render leaks raw HTML/CSS, editor placeholders, malformed Gutenberg output, or broken mobile product/table layouts despite clean stored content.
