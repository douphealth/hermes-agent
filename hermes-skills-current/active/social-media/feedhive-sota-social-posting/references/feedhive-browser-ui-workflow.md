# FeedHive browser UI workflow notes

Session-derived notes for using the authenticated FeedHive web app when REST API cannot access a feature such as AI image generation.

## Login / session

- Open `https://app.feedhive.com/` or `https://app.feedhive.com/signin`; `/sign-in` and `/login` can show FeedHive error/support pages.
- Email/password login can silently appear to do nothing with normal browser clicks. If the page stays on `/signin` with no visible error, inspect the button's React props and call its `onClick` handler directly.
- Do not print, persist, or include credentials/API keys in notes or replies. Use `[REDACTED]` for any copied secret.

## React click workaround

Use only when normal `browser_click` does not trigger an SPA action even though the button is enabled:

```js
(() => {
  const btn = Array.from(document.querySelectorAll('button'))
    .find(b => b.innerText.includes('Sign in') || b.innerText.includes('Create image with AI'));
  const k = Object.keys(btn).find(k => k.startsWith('__reactProps'));
  btn[k].onClick({ preventDefault(){}, stopPropagation(){}, currentTarget: btn, target: btn });
  return 'react-click';
})()
```

## AI image generation flow

1. Navigate to `/compose` after login.
2. Enter the post text first. The quick image-generation button is disabled until there is post content.
3. Click `quick-ai-image-generate` or the `Create image with AI` tile.
4. If the tile does not open, use the React click workaround on the button whose text includes `Create image with AI`.
5. Modal fields observed:
   - `Prompt*`
   - `Aspect ratio` default/available `1:1`
   - optional reference images, up to 3
   - `Use in post` disabled until generation succeeds
   - `Generate` enabled after prompt is filled
6. For high-quality social images, prompt for a clean base visual with no text/logos. Add headline/branding later with controlled HTML/SVG typography.

## Example prompt

```text
Premium editorial product photo, modern black massage gun on a dark gym bench, subtle athletic recovery setting, dramatic softbox lighting, clean luxury fitness aesthetic, shallow depth of field, no text, no logos, square composition, photorealistic, high detail
```

## Known boundaries

- FeedHive REST API key can create posts/media/social operations, but does not expose AI image generation.
- Web image generation requires an authenticated browser session and may consume FeedHive AI credits or connected Replicate billing.
