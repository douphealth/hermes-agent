# Premium SOTA Post Header Design Reference

## Design Philosophy

Clean, minimal, premium. No borders that look "cheap." Card-based layout with subtle shadows, proper typography, and responsive scaling. Think Stripe docs, Linear blog, Vercel — not generic WordPress.

## CSS Architecture

### Card (top-level container)
```css
.sota-root {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
  max-width: 728px;
  margin: 2.5rem auto 1.5rem;
  padding: 0 1rem;
}
.sota-card {
  background: #fff;
  border-radius: 20px;
  padding: 2rem 2rem 1.5rem;
  box-shadow: 0 1px 2px rgba(0,0,0,.04), 0 8px 24px rgba(0,0,0,.06);
  border: 1px solid #f0f0f0;
}
```

### Author Row — avatar + stacked name/date
```css
.sota-author-row {
  display: flex;
  align-items: center;
  gap: .75rem;
  margin-bottom: 1rem;
}
.sota-avatar {
  width: 44px; height: 44px;
  border-radius: 50%;
  object-fit: cover;
  border: 2px solid #fff;
  box-shadow: 0 0 0 2px #e8e8e8, 0 4px 12px rgba(0,0,0,.08);
  flex-shrink: 0;
}
.sota-author-info { display: flex; flex-direction: column; }
.sota-author-name { font-size: 15px; font-weight: 600; color: #111; letter-spacing: -.01em; }
.sota-meta-line { display: flex; align-items: center; gap: 6px; font-size: 13px; color: #888; }
```

### Breadcrumbs — minimal with subtle separators
```css
.sota-bread { font-size: 13px; color: #999; margin-bottom: .85rem; }
.sota-bread a { color: #666; text-decoration: none; }
.sota-bread a:hover { color: #111; }
.sota-bread .breadcrumb_last { color: #333; font-weight: 500; }
```

### Badges — pill-shaped, colored
```css
.sota-time {  /* Reading time — purple accent */
  font-size: 12px; font-weight: 600;
  color: #7c3aed; background: #f5f3ff;
  padding: 4px 12px; border-radius: 20px;
}
.sota-cat {  /* Category badges — neutral gray */
  font-size: 12px; font-weight: 500;
  color: #555; background: #f5f5f5;
  padding: 4px 12px; border-radius: 20px;
  text-decoration: none;
}
.sota-cat:hover { background: #eee; color: #111; }
.sota-updated { font-size: 12px; color: #aaa; }
```

### Disclosure — warm off-white card
```css
.sota-disclosure {
  background: #fafaf9;
  border: 1px solid #f0eee6;
  border-radius: 14px;
  padding: 14px 18px;
  margin: 2rem auto;
  max-width: 728px;
  font-size: 13px;
  color: #666;
  line-height: 1.5;
  display: flex;
  align-items: flex-start;
  gap: 10px;
}
```

## Responsive Breakpoints

```css
@media(max-width: 640px) {
  .sota-root { margin: 1.5rem auto 1rem; padding: 0 .75rem; }
  .sota-card { padding: 1.25rem 1rem 1rem; border-radius: 16px; }
  .sota-avatar { width: 36px; height: 36px; }
  .sota-author-name { font-size: 14px; }
  .sota-meta-line { font-size: 12px; }
  .sota-bread { font-size: 12px; }
  .sota-time { font-size: 11px; padding: 3px 10px; }
  .sota-cat { font-size: 11px; padding: 3px 10px; }
  .sota-updated { font-size: 11px; }
  .sota-disclosure { padding: 12px 14px; font-size: 12px; border-radius: 12px; }
}
```

## Color Palette

| Element | Hex | Usage |
|---------|-----|-------|
| Card bg | `#ffffff` | Container background |
| Border | `#f0f0f0` | Subtle card border |
| Shadow | `rgba(0,0,0,.04)` + `.06` | Card box-shadow |
| Author name | `#111111` | Primary text |
| Meta text | `#888888` | Secondary text (dates) |
| Breadcrumb link | `#666666` | Navigation |
| Breadcrumb hover | `#111111` | Hover state |
| Reading time bg | `#f5f3ff` | Purple pill background |
| Reading time text | `#7c3aed` | Purple accent |
| Category bg | `#f5f5f5` | Gray pill background |
| Category text | `#555555` | Gray text |
| Disclosure bg | `#fafaf9` | Warm off-white |
| Disclosure border | `#f0eee6` | Warm border |

## Avoiding Common Design Pitfalls

- **No thick/heavy borders.** Use `1px solid #f0f0f0` not `#ddd` or `#ccc`. The border should be barely visible.
- **Shadows should be subtle.** Two-layer shadow (`0 1px 2px rgba(0,0,0,.04)` + `0 8px 24px rgba(0,0,0,.06)`) creates depth without heaviness.
- **No solid dividers.** Use gradient fades: `background: linear-gradient(to right, transparent, #eee 10%, #eee 90%, transparent)`.
- **Avatar ring.** Double-shadow creates a photo ring effect: `box-shadow: 0 0 0 2px #e8e8e8, 0 4px 12px rgba(0,0,0,.08)`.
- **Font stack.** Use system fonts (`-apple-system, BlinkMacSystemFont, 'Segoe UI'...`) for native performance — no Google Fonts import needed unless the site already uses one.
- **Pill padding.** Badges should have `4px 12px` (top/bottom, left/right) — not too tight, not too loose.
- **Mobile adjustments.** Every size should scale down proportionally at 640px breakpoint. Don't just hide elements — shrink them.
