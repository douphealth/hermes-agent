---
name: feedhive-sota-social-posting
description: "Create and schedule SOTA social media posts for all 8 WP sites via FeedHive API"
version: 1.0.0
author: Hermes Agent
metadata:
  hermes:
    tags: [feedhive, social-media, scheduling, wordpress]
    category: social-media
---

# FeedHive SOTA Social Posting

Use this skill to create high-quality social media posts for all 8 WordPress sites and schedule them via FeedHive API.

## Connected Accounts (FeedHive)

| Account | Platform | ID | Status |
|---------|----------|----|--------|
| Affiliate Marketing for Success | Facebook | `27b5da84-19a9-4a52-b6ad-82c433dd4b2e` | ✅ Active |
| affiliatemarketingforsuccess | Instagram | `ddf93e5d-15ca-441c-9427-8350365a101e` | ✅ Active |
| Gear Up to Fit | Instagram | `3b26b23e-4895-438b-a9be-f4f758500821` | ✅ Active |
| Gear Up to Fit | Facebook | `c481868d-2d5e-4565-a2dc-29b994fd0d30` | ✅ Active |
| Alexis Papaioannou | LinkedIn | `05699dae-c4c1-4af7-993d-bb391c34cef2` | ❌ Needs reconnect |
| GearUptoFit | LinkedIn | `7c10e9b5-fd91-4205-b8eb-13c2ec0e2b78` | ❌ Needs reconnect |

## API Details

- **Base URL:** `https://api.feedhive.com`
- **Auth:** `Authorization=[REDACTED] {API_KEY}`
- **API Key:** In secrets file at `/home/hermes/.secrets/alexiios-websites-credentials.txt` under `[SOCIAL MEDIA APPS]` → FeedHive

## Steps

### 1. Get latest content from all sites

```python
import requests
sites = [
    'gearuptofit.com', 'affiliatemarketingforsuccess.com', 'frenchyfab.com',
    'mysticaldigits.com', 'micegoneguide.com', 'gearuptogrow.com',
    'plantastichaven.com', 'efficientgptprompts.com'
]
for site in sites:
    r = requests.get(f'https://{site}/wp-json/wp/v2/posts?per_page=3&_fields=title,link,excerpt,date', timeout=15)
    if r.status_code == 200:
        posts = r.json()
        for p in posts:
            print(f"{site} | {p['title']['rendered'][:60]} | {p['link']}")
```

### 2. Create posts in FeedHive

```python
import requests, json
# Load API key from the local secrets file; never hardcode or print it.
api_key=[REDACTED]
h = {"Authorization": f"Bearer {api_key}", "Accept": "application/json", "Content-Type": "application/json"}

FB_GUTF = "c481868d-2d5e-4565-a2dc-29b994fd0d30"
IG_GUTF = "3b26b23e-4895-438b-a9be-f4f758500821"
FB_AMFS = "27b5da84-19a9-4a52-b6ad-82c433dd4b2e"
IG_AMFS = "ddf93e5d-15ca-441c-9427-8350365a101e"

payload = {
    "text": "Post text here with link",
    "accounts": [FB_GUTF, IG_GUTF],  # or [FB_AMFS, IG_AMFS]
    "status": "draft",
    "publish_type": "regular"
}
r = requests.post("https://api.feedhive.com/posts", headers=h, json=payload)
```

### 3. Schedule posts

```python
# Get all drafts
r = requests.get("https://api.feedhive.com/posts?status=draft&limit=30", headers=h)
drafts = r.json()

# Schedule at optimized times
times = ['09:00', '13:00', '17:00']  # Mon-Fri, weekdays only
for i, item in enumerate(drafts['data']['items']):
    post_id = item['id']
    # Calculate datetime
    payload = {"status": "scheduled", "scheduled_at": datetime_str}
    requests.patch(f"https://api.feedhive.com/posts/{post_id}", headers=h, json=payload)
```

### 4. Post templates by site

**GearUpToFit** (Fitness/Running) → FB_GUTF, IG_GUTF
- Product reviews: "We tested [product]. Here's our verdict..."
- Training guides: "[Topic] — the complete science-backed protocol..."
- Health content: "New research on [topic]..."

**AffiliateMarketingForSuccess** → FB_AMFS, IG_AMFS
- Affiliate network reviews: "[Network] review — is it worth it for publishers?"
- How-to guides: "Step-by-step [topic] for affiliate marketers"
- AI prompts: "AI prompt templates for [use case]..."

**GearUpToGrow** → FB_GUTF, IG_GUTF
- Productivity comparisons: "[Method A] vs [Method B] — which works best?"
- Focus/deep work: "How to [solve productivity problem]..."

**EfficientGPTPrompts** → FB_AMFS, IG_AMFS
- Prompt templates: "[Use case] prompt templates for [audience]..."
- AI workflows: "AI workflow prompts for [role]..."

**PlantasticHaven** → FB_GUTF, IG_GUTF
- Plant care guides: "[Plant] problems? Here's how to fix..."
- Beginner guides: "New to houseplants? Start here..."

**MysticalDigits** → FB_GUTF, IG_GUTF
- Numerology calculators: "What's your [number type]? Calculate in 3 minutes..."
- Spiritual guides: "Understanding [topic] in numerology..."

**MiceGoneGuide** → FB_GUTF, IG_GUTF
- Pest control guides: "How to [solve pest problem] safely..."
- Prevention tips: "[Pest] prevention checklist for homeowners..."

## FeedHive AI image generation

- FeedHive has built-in AI image generation in the web app: "Create image with AI".
- Current public pricing/features copy says image generation uses **Flux Pro** and **Nana Banana** directly from FeedHive.
- FeedHive docs also support adding a user's own Replicate API key under Settings → Replicate Integration; then image generation bills to the user's Replicate account. OpenAI API key integration is for AI writing/credits, not necessarily GPT Image 2.0.
- AI-generated images consume FeedHive AI credits (pricing page text observed: roughly 20-25 AI credits per image; may vary by plan/model).
- The REST API key works for `/status`, `/socials`, `/posts`, and `/media/uploads`, but the documented REST API does **not** expose an AI image-generation endpoint. Web-app AI image generation uses authenticated AppSync/Cognito GraphQL (`createAIImage`, `getAIImageGeneration`) and requires valid FeedHive web login/session, not just the public FeedHive REST API key.
- Practical browser flow after login: open `/compose`, enter post text first, then the quick `quick-ai-image-generate` button becomes enabled. If the visible "Create image with AI" tile does not open via normal click, invoke its React `onClick` handler from the console; this opened the modal reliably in-session.
- In the image modal, use a base-image prompt with **no text/logos** and 1:1 aspect ratio, then click Generate and Use in post. Example prompt: `Premium editorial product photo, modern black massage gun on a dark gym bench, subtle athletic recovery setting, dramatic softbox lighting, clean luxury fitness aesthetic, shallow depth of field, no text, no logos, square composition, photorealistic, high detail`.
- See `references/feedhive-ai-image-generation-notes.md` for probes, GraphQL operation shapes, and the practical unblock workflow.
- See `references/feedhive-browser-ui-workflow.md` for the authenticated browser workflow and UI quirks discovered during the FeedHive image-generation test.
- See `references/gearuptofit-tool-promotion-playbook.md` for the GearUpToFit free-tools campaign sequence, GPT Images prompt, and IG/FB copy direction.

## Creative quality workflow

- FeedHive's built-in AI image generation can produce low-quality/generic infographic-style visuals; use it only for quick drafts or if the output passes strict visual QA. For SOTA/enterprise social assets, prefer GPT Images/OpenAI/FAL/Replicate for the **base image**, then add exact typography separately via controlled HTML/SVG/Canva-style layout.
- Do **not** ask image models to render the final social text unless intentionally testing; raw model typography is unreliable. Generate clean base art with `no text, no logos, no UI, no labels`, then overlay the hook/headline/CTA yourself.
- For blog traffic posts, avoid putting the full URL prominently inside the image. It usually looks cheap and hurts design. Put the URL in the caption/post body; keep image text to hook + benefit + brand/CTA.
- User expects blunt, exact creative critique: say if the visual is not acceptable, identify exact problems, then provide exact improved prompt, exact overlay copy, and exact caption.
- When the user sends iterative image drafts and asks “is this better?” or “what exactly should I improve?”, answer with concrete visual deltas only: hierarchy, safe margins, product clarity, negative space, mobile readability, CTA strength, and whether to post/regenerate. Avoid long theory.
- IG/FB feed standard: square 1080x1080 works for Instagram feed and Facebook feed; keep key text away from edges, move CTA/brand above bottom safe margin, put links in captions, and create separate 1080x1920 assets for Stories/Reels. Facebook captions can be longer and should use fewer hashtags than Instagram.
- Recommended massage-gun style for GearUpToFit: dark premium recovery-studio product photo, massage gun sharp on right/lower-right, clean negative space on left, warm orange rim light, realistic athlete recovery pose blurred in background. Overlay: `MOST PEOPLE USE / MASSAGE GUNS / WRONG`, subhead `3 recovery mistakes slowing your recovery`, CTA `COMPARE THE TOP PICKS →`, brand `GEARUPTOFIT`.
- Recommended massage-gun style for GearUpToFit: dark premium recovery-studio product photo, massage gun sharp on right/lower-right, clean negative space on left, warm orange rim light, realistic athlete recovery pose blurred in background. Overlay: `MOST PEOPLE USE / MASSAGE GUNS / WRONG`, subhead `3 recovery mistakes that waste your time`, CTA `Save this before your next leg day →`, brand `GearUpToFit`.
- For GearUpToFit tool promotion, prioritize RunMatch AI Shoe Finder (`/shoe-finder/`) as a mini-campaign before broad hub/tool-bundle posts. It has clearer buyer intent and stronger social hooks than generic “fitness tools” messaging. Winning first-post hook: `STOP BUYING / RUNNING SHOES / BLIND`, subhead `Find a smarter match for your feet, mileage & terrain`, CTA `TRY RUNMATCH AI →`. Pair generic unbranded running shoes with an abstract phone/AI-match card so the image sells the tool, not a specific shoe brand. See `references/gearuptofit-runmatch-social-creative.md`.

## Pitfalls

- Labels must be valid UUIDs from the FeedHive account
- Post without accounts is OK as draft, but schedule requires accounts
- frenchyfab.com is DOWN (HTTP 500) — WordPress fatal error. Fix: try disabling Seraphinite Accelerator first via REST API `/wp/v2/plugins/`. If still 500, plugins with spaces/special chars in filenames (Enhanced-Auto-Image-Generator, query-hunter, Auto-Featured-Image-Finder) won't deactivate via standard REST API — use Code Snippets API or hosting panel (CyberPanel) to create mu-plugin or rename directories.
- LinkedIn accounts need manual browser reconnection (token expired)
- Schedule requires `accounts` and `scheduled_at` together
- Instagram posts without images won't perform well — always add image
- FeedHive API key is in secrets under `[SOCIAL MEDIA APPS]` → FeedHive
- If FeedHive is in onboarding/get-started flow, Studio mode is blocked. Complete onboarding via browser or use direct API posting instead.
- FeedHive API base: `https://api.feedhive.com`, auth: `Authorization=[REDACTED] {key}`
- FeedHive API may close connections during rapid batch draft creation (`RemoteDisconnected`). Use `Connection: close`, 0.8-2s pacing, and 3-4 retries per post; then verify exact draft captions with `GET /posts?status=draft&limit=100` before reporting success.
