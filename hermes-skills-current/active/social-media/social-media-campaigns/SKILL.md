---
name: social-media-campaigns
description: "Plan, draft, approve, schedule, and verify social media campaigns across connected schedulers and social accounts."
version: 1.0.0
author: Hermes Agent
metadata:
  hermes:
    tags: [social-media, content-marketing, scheduling, feedhive, facebook, instagram, approval-workflow]
    category: social-media
    related_skills: [humanizer, authority-engine, xitter, xurl]
---

# Social media campaigns

Use this skill when the user asks to create, repurpose, schedule, publish, or choose tools for social posts, especially for website promotion, affiliate content, SEO-driven brands, or multi-platform campaigns.

## Hard rules for this user (Alexiios — 8 WP sites)

1. **NO approval gate.** When user says "proceed"/"create"/"post"/"fix it" → execute immediately. Do not ask for approval first. Create drafts + schedule in one pass.
2. **Do not guess the social tool.** The user has Metricool + FeedHive + Publer + SocialBee + PromoRepublic + Robolly + MyMarky + Radaar + Missinglettr + Ocoya. All credentials in secrets file. Prefer FeedHive (has active API key and connected FB/IG accounts).
3. **Act fast when corrected.** User rage is a signal you missed something. Immediately check credentials file, session history, or the skill library. Do not explain.
4. **Do not expose credentials.** Report only provider names, account labels, status. Never print API keys, tokens, passwords.
5. **Execute batch — never single post.** Create 10-14 posts at once across all sites, then schedule them across the week. Single-post workflows waste time.

## Tool-selection workflow

When asked "what is the best tool?" for social posts:

1. Load this skill plus:
   - `humanizer` for natural, non-AI copy
   - `authority-engine` for SEO/GEO/AEO/topic-authority promotion when promoting websites/blog content
   - `xitter` or `xurl` only for direct X/Twitter execution
2. Check available credentials/connectors before answering:
   - Search current environment/secret files for provider labels without printing values.
   - Use `session_search` for prior platform/account setup notes.
   - If Hermes Agent configuration/tooling is involved, load `hermes-agent` before advising setup.
3. Prefer the already-connected scheduler over generic recommendations.
4. State account limitations clearly, e.g. "LinkedIn reconnect needed," but do not let that block drafts for connected channels.

## Drafting workflow

For website/social promotion:

1. Open the target URL with browser or HTTP and extract the real value proposition, CTAs, claims, and page structure.
2. If the user asks for “very high quality,” “viral,” “SOTA,” or says they want to “check first,” produce one approval-ready sample before building the full batch or scheduling. Include platform, goal, exact link, post copy, visual/carousel/Reel concept, and one shorter platform variant. Do not publish.
3. When choosing between promoting a generic hub/tool bundle and a specific high-intent tool, prefer a focused mini-campaign around the clearest buyer-intent asset first. For GearUpToFit, `/shoe-finder/` is usually the strongest first target: running shoes are visual, pain-driven, and affiliate/commercially adjacent. Create multiple distinct posts around mistakes, terrain, budget, support, and quiz/tool angles rather than repeating the same post.
4. If the user approves the sample but asks “how do we proceed now?” explain the execution pipeline first instead of immediately generating assets or scheduling: content batch → visual production method → draft creation → review/approval → FeedHive scheduling → verification. Make clear which steps are drafts vs live publishing.
4. Before producing social visuals, state the asset route when it materially affects quality: AI-generated base image via configured provider, controlled SVG/HTML typography overlay, or manual vector fallback. For enterprise social graphics with exact hook text, prefer AI/background + controlled typography overlay; do not rely on raw AI image generation for exact text.
5. Choose a platform-specific angle:
   - Facebook: useful, conversational, community-oriented, link-friendly. Use longer explanatory captions when useful, but keep hashtags minimal (often 2–4).
   - Instagram: hook + short body + visual/carousel idea + CTA; do not rely on clickable body links except bio/story context. Square 1080x1080 is fine for feed; use separate 1080x1920 assets for Stories/Reels.
   - X/Twitter: concise hook, punchy thread or single post; use `xitter`/`xurl` if posting is approved.
   - LinkedIn: professional insight, founder/operator angle, no hype. Only schedule if account is connected.
4. Write posts with a strong first line, specific claims, and one clear CTA.
5. Avoid AI tells: "unlock," "game-changing," "ultimate guide," generic rule-of-three, mechanical bold headers, and emoji clutter unless the brand style calls for it.
6. For affiliate marketing content, emphasize useful systems: niche selection, search intent, content quality, product fit, email capture, comparison logic, proof, limitations, and topical authority.

## FeedHive API direct scheduling (Alexiios — preferred method)

For this user, always use FeedHive API directly instead of browser-based scheduling.

### Connected accounts (FeedHive API)
- FB_GUTF = "c481868d-2d5e-4565-a2dc-29b994fd0d30"   # Gear Up to Fit Facebook
- IG_GUTF = "3b26b23e-4895-438b-a9be-f4f758500821"   # Gear Up to Fit Instagram
- FB_AMFS = "27b5da84-19a9-4a52-b6ad-82c433dd4b2e"  # Affiliate Marketing for Success Facebook
- IG_AMFS = "ddf93e5d-15ca-441c-9427-8350365a101e"   # Affiliate Marketing for Success Instagram
- LinkedIn (both) = failed, skip

### API details
- Base: `https://api.feedhive.com`
- Auth: `Authorization=[REDACTED] {API_KEY}` (key in secrets file under `[SOCIAL MEDIA APPS]` → FeedHive)
- GET /status → verify auth
- GET /socials → list connected accounts
- GET /posts?status=draft → list drafts
- POST /posts → create post
- PATCH /posts/{id} → update/schedule post

### Post creation
```python
payload = {
    "text": "Post text with link",
    "accounts": [FB_GUTF, IG_GUTF],  # or [FB_AMFS, IG_AMFS]
    "status": "draft",
    "publish_type": "regular"
}
```

### Scheduling optimized times
Create across the coming week at: Mon-Fri 09:00, 13:00, 17:00 UTC.
Schedule via PATCH: `{"status": "scheduled", "scheduled_at": "ISO8601"}`

### Post template by site type
- **GearUpToFit (Fitness/Running)** → FB_GUTF + IG_GUTF: Reviews ("We tested [product]"), training guides, health content
- **AffiliateMarketingForSuccess** → FB_AMFS + IG_AMFS: Network reviews, how-to guides, AI prompt templates
- **GearUpToGrow (Productivity)** → FB_GUTF + IG_GUTF: Method comparisons, focus/deep work
- **EfficientGPTPrompts** → FB_AMFS + IG_AMFS: Prompt templates, AI workflows
- **PlantasticHaven (Plants)** → FB_GUTF + IG_GUTF: Plant care, beginner guides
- **MysticalDigits (Numerology)** → FB_GUTF + IG_GUTF: Life path calculators, spiritual guides
- **MiceGoneGuide (Pest Control)** → FB_GUTF + IG_GUTF: Safe cleanup, prevention

### DNS workaround
WSL DNS may fail for `api.feedhive.io`. Use `api.feedhive.com` instead (Cloudflare CDN, resolves fine). Python requests work even when curl + browser fail.

After explicit user approval:

1. If the approval is context-specific (e.g. “Post it” after a prepared AMFS post/image), infer the previously discussed platform/account when obvious and execute instead of asking broad clarification.
2. Confirm target platform(s), account(s), timezone, and schedule time only when missing or materially ambiguous.
3. Locate required media deterministically before opening the scheduler: check the uploaded file if available, then likely Windows Downloads/Desktop paths, and verify candidate filenames/dimensions with `file`, `identify`, or another installed CLI without requiring PIL.
4. Create/schedule through the confirmed provider API/tool.
5. Save returned post IDs and scheduled timestamps in the session response only; do not write credentials to files.
6. Verify the scheduled item exists in the provider response. If live-published, verify public URL if available.
7. If the scheduler is logged out and no token exists, state the exact blocker concisely and ask only for the missing access method, not for a new creative decision.

## Pitfalls

- Do not answer with generic scheduler suggestions when the user has already provided social software credentials. Check first.
- When the user asks what is needed to proceed after a credential/session blocker, answer with the shortest concrete unblock list first. Avoid long explanations; name the exact missing access method and the fastest option.
- A user being logged into FeedHive in their own browser does **not** mean the Hermes browser session is logged in. Verify the live Hermes browser session before using web-only FeedHive features.
- FeedHive REST API access is not the same as FeedHive web-app access. The REST API works for `/status`, `/socials`, `/posts`, and `/media/uploads`, but FeedHive AI image generation is a web-app/AppSync/Cognito feature and may require a valid web session.
- If FeedHive opens `/get-started`, onboarding can block Studio/Compose even when API accounts are connected. Complete/skip onboarding in the Hermes browser session before trying web-only tools like AI image generation.
- Do not say browser/API automation is unavailable until local paths, prior session context, provider docs, and direct API probes have been checked.
- Do not publish to LinkedIn if previous state says reconnect-needed.
- Do not turn every post into a sales pitch. For AMFS-style affiliate marketing, the strongest posts usually teach one useful idea, then route to the relevant hub.
- Do not promise virality. Produce viral-style hooks and high-shareability structure, but frame outcomes honestly.
- Do not surprise-create assets when the user is asking about process/tooling. If the user says “wait,” “first,” or asks how an image/tool works, stop execution and answer that operational question directly.
- Do not treat a missing image-generation credential as proof that image generation is low quality or unavailable permanently. Explain setup state separately from model quality, and recommend the durable quality workflow: AI visual base plus deterministic typography/layout overlay.

## FeedHive API direct scheduling

- `references/feedhive-amfs-account-context.md` — current known FeedHive/AMFS account context and approval rule learned from prior sessions.
