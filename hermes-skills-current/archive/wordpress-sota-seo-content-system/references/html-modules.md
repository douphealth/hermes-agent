# Premium WordPress HTML Modules

Use these patterns inside `<!-- wp:html -->` wrappers when a page needs premium visual structure without becoming fragile.

## 1. Intent Note
```html
<!-- wp:html -->
<div class="wsota-intent" style="margin:0 0 22px;padding:14px 16px;border-left:4px solid #2f6b3b;background:#f3f8f1;border-radius:8px;line-height:1.75;">
  <strong>Quick answer:</strong> State the answer in plain English immediately, then guide the reader into the fuller explanation.
</div>
<!-- /wp:html -->
```

## 2. Editorial Note
```html
<!-- wp:html -->
<div class="wsota-editorial" style="border:1px solid #d8e3d5;border-radius:12px;padding:14px 16px;margin:0 0 24px;background:#f8fbf6;font-size:0.98rem;line-height:1.7;">
  <strong>Editorial note:</strong> This guide is reviewed for clarity, practical accuracy, and beginner usefulness. See our <a href="/about/">about page</a>, <a href="/editorial-policy/">editorial policy</a>, and <a href="/review-methodology/">review methodology</a>.
</div>
<!-- /wp:html -->
```

## 3. Comparison Table
```html
<!-- wp:html -->
<table>
  <thead>
    <tr><th>Option</th><th>Best For</th><th>Difficulty</th><th>Main Drawback</th></tr>
  </thead>
  <tbody>
    <tr><td>Option A</td><td>Beginners</td><td>Easy</td><td>Slower results</td></tr>
    <tr><td>Option B</td><td>Advanced users</td><td>Moderate</td><td>Needs more maintenance</td></tr>
  </tbody>
</table>
<!-- /wp:html -->
```

## 4. Scenario Section
```html
<!-- wp:html -->
<section class="wsota-scenarios" style="margin:28px 0 22px;padding:18px 20px;border:1px solid #e4e8ee;border-radius:14px;background:#fbfcfe;">
  <h2 style="margin-top:0;font-size:24px;">Best by Scenario</h2>
  <h3>Office</h3>
  <p>Explain what works in this situation and why.</p>
  <h3>Bathroom</h3>
  <p>Explain what changes in this environment.</p>
  <h3>Bedroom</h3>
  <p>Explain what matters most here.</p>
</section>
<!-- /wp:html -->
```

## 5. Mistake Box
```html
<!-- wp:html -->
<div class="wsota-warning" style="margin:24px 0;padding:16px 18px;border-radius:12px;background:#fff8ef;border:1px solid #ecd9bc;line-height:1.75;">
  <strong>Common mistake:</strong> State the mistake bluntly, then explain the better move.
</div>
<!-- /wp:html -->
```

## 6. Next-Step CTA
```html
<!-- wp:html -->
<section class="wsota-next" style="margin:26px 0 8px;padding:18px 20px;border-radius:14px;background:#1f2937;color:#fff;">
  <h2 style="margin-top:0;color:#fff;font-size:24px;">Next Step</h2>
  <p style="margin-bottom:0;line-height:1.75;">Guide the reader to the most logical next article, checklist, calculator, or category page.</p>
</section>
<!-- /wp:html -->
```

## Rules
- Keep modules visually restrained.
- Prefer spacing, borders, and background tone over flashy effects.
- If the theme is unstable, downgrade to simpler markup immediately.
- Verify live on mobile-sized layouts whenever possible.
