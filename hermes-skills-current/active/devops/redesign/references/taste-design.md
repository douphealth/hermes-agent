<!-- Consolidated from skill: taste-design; original path: /home/hermes/.hermes/skills/devops/taste-design -->

---
name: taste-design
description: Senior UI/UX Engineer for premium frontend. Configurable design dials (variance 8, motion 6, density 4). Enforces metric-based rules, hardware-accelerated CSS, anti-AI-slop patterns, and balanced design engineering. Works with any CSS framework including vanilla CSS on WordPress sites.
version: 1.0.0
author: Adapted from taste-skill by Leonxlnx for Hermes Agent
---

# High-Agency Design Skill

## 1. ACTIVE BASELINE CONFIGURATION
* DESIGN_VARIANCE: 8 (1=Perfect Symmetry, 10=Artsy Chaos)
* MOTION_INTENSITY: 6 (1=Static/No movement, 10=Cinematic/Magic Physics)
* VISUAL_DENSITY: 4 (1=Art Gallery/Airy, 10=Pilot Cockpit/Packed Data)

**AI Instruction:** The standard baseline for all generations is strictly set to these values (8, 6, 4). Always listen to the user and adapt these values dynamically based on explicit requests. Use these as global variables to drive logic in Sections 3 through 7.

## 2. DEFAULT ARCHITECTURE & CONVENTIONS

* **DEPENDENCY VERIFICATION:** Before importing ANY 3rd party library, check what's available in the project. Never assume a library exists.
* **WordPress/Kadence Context:** When working with WordPress sites, respect the existing theme (Kadence). Use inline CSS in HTML blocks, keep custom CSS scoped, and never break template hierarchy.
* **WordPress content rewriting:** If the task is specifically to upgrade article/page content inside WordPress rather than redesign a standalone UI, also load `wordpress-sota-seo-content-system`. Use this design skill for polish and visual taste, but let the WordPress SOTA skill control rewrite structure, schema, internal links, and HTML module safety.
* **Styling Policy:** Use Tailwind CSS for 90% of standalone projects. For WordPress inline blocks, use scoped `<style>` tags with specific class prefixes to avoid conflicts.
* **ANTI-EMOJI POLICY:** NEVER use emojis in code, markup, text content, or alt text. Replace with quality icons (Phosphor, Radix) or clean SVG primitives.
* **Responsiveness & Spacing:**
  * Standardize breakpoints (sm, md, lg, xl).
  * Contain page layouts using max-w-[1400px] mx-auto or max-w-7xl.
  * NEVER use h-screen for full-height sections. ALWAYS use min-h-[100dvh].
  * NEVER use complex flexbox percentage math. ALWAYS use CSS Grid.
* **Icons:** Use @phosphor-icons/react or clean inline SVGs. Standardize strokeWidth globally (1.5 or 2.0).

## 3. DESIGN ENGINEERING DIRECTIVES (Bias Correction)

**Rule 1: Deterministic Typography**
* Display/Headlines: text-4xl md:text-6xl tracking-tighter leading-none.
* ANTI-SLOP: Discourage Inter for premium/creative contexts. Force Geist, Outfit, Cabinet Grotesk, or Satoshi.
* Serif fonts banned for Dashboard/Software UIs. Use Geist + Geist Mono or Satoshi + JetBrains Mono.
* Body: text-base text-gray-600 leading-relaxed max-w-[65ch].

**Rule 2: Color Calibration**
* Max 1 Accent Color. Saturation < 80%.
* THE LILA BAN: AI Purple/Blue is strictly BANNED. Use Zinc/Slate with high-contrast accents (Emerald, Electric Blue, Deep Rose).
* COLOR CONSISTENCY: Stick to one palette. Do not fluctuate between warm and cool grays.

**Rule 3: Layout Diversification**
* ANTI-CENTER BIAS: Centered Hero/H1 sections BANNED when DESIGN_VARIANCE > 4. Force Split Screen, Left Aligned/Right Asset, or Asymmetric White-space.

**Rule 4: Materiality and Anti-Card**
* DASHBOARD HARDENING: For VISUAL_DENSITY > 7, generic cards BANNED. Use border-t, divide-y, or negative space.
* Use cards ONLY when elevation communicates hierarchy. Tint shadows to background hue.

**Rule 5: Interactive UI States**
* Loading: Skeletal loaders matching layout (no generic spinners).
* Empty: Composed states showing how to populate data.
* Error: Clear inline error reporting.
* Tactile: On :active, use -translate-y-[1px] or scale-[0.98].

**Rule 6: Data & Form Patterns**
* Labels above inputs. Helper text optional. Error text below. Standard gap-2.

## 4. CREATIVE PROACTIVITY (Anti-Slop)

* **Liquid Glass:** Add 1px inner border and subtle inner shadow for physical edge refraction.
* **Magnetic Micro-physics:** For MOTION_INTENSITY > 5, implement buttons pulling toward cursor.
* **Perpetual Micro-Interactions:** Embed continuous micro-animations (pulse, float, shimmer) for MOTION_INTENSITY > 5.
* **Staggered Orchestration:** Never mount lists instantly. Use cascade reveals with animation-delay.

## 5. PERFORMANCE GUARDRAILS
* Grain/noise on fixed pointer-events-none pseudo-elements only.
* Animate via transform and opacity only. Never top/left/width/height.
* Z-index restraint: Never spam z-50 or z-10 arbitrarily.

## 6. THE CREATIVE ARSENAL

Pull from these when appropriate:
* **Navigation:** Mac OS Dock magnification, magnetic buttons, dynamic island, contextual radial menus
* **Layouts:** Bento Grid, Masonry, Chroma Grid, Split Screen Scroll, Curtain Reveal
* **Cards:** Parallax Tilt, Spotlight Border, Glassmorphism, Holographic Foil
* **Scroll:** Sticky Stack, Horizontal Scroll Hijack, Zoom Parallax, SVG Path Drawing
* **Micro-interactions:** Particle buttons, Directional hover aware, Ripple click, Animated SVG line drawing, Mesh gradient backgrounds

## 7. AI TELLS (Forbidden Patterns)

- No neon/outer glows, use inner borders or subtle tinted shadows
- No pure black #000000. Use Zinc-950 or Charcoal
- No Inter font. Use Geist, Outfit, Cabinet Grotesk, or Satoshi
- No oversized H1s. Control hierarchy with weight and color
- No 3-column equal card layouts. Use zig-zag, asymmetric grid, or horizontal scroll
- No generic names (John Doe, Acme, Nexus). Use creative, realistic names
- No fake round numbers (99.99%, 50%). Use organic data (47.2%)
- No AI copywriting cliches (Elevate, Seamless, Unleash, Next-Gen)
- No broken Unsplash links. Use picsum.photos/seed/{random}/800/600
- No emojis anywhere

## 8. MOTION-ENGINE BENTO PARADIGM

For modern SaaS dashboards:
* Background #f9fafb. Cards #ffffff with 1px border-slate-200/50
* Rounded-[2.5rem] for major containers with diffusion shadow
* Spring physics: type: spring, stiffness: 100, damping: 20
* Labels outside and below cards for gallery-style presentation
* Labels and descriptions must be placed outside and below cards
* Every card must have an active state that loops infinitely

## 9. FINAL PRE-FLIGHT CHECK
- Mobile layout collapse guaranteed for high-variance designs
- Full-height sections use min-h-[100dvh] not h-screen
- Empty, loading, and error states provided
- Cards omitted in favor of spacing where possible
- No banned patterns from Section 7 present
