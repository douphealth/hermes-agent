# FeedHive AI image generation notes

Session-derived provider notes for future FeedHive social-post work.

## What FeedHive exposes

- FeedHive web app has a "Create image with AI" flow in Compose/Studio.
- Public feature/pricing copy observed in app JS says AI image generation uses **Flux Pro** and **Nana Banana**.
- FeedHive docs include:
  - `Content Creation / Adding your OpenAI API Key`: OpenAI key can bypass FeedHive AI credit limit for AI-powered features using the user's OpenAI account.
  - `Content Creation / Adding your Replicate API Key`: Replicate key is used for AI image generation requests and bills through the user's Replicate account.
- Pricing copy observed: AI-generated image uses roughly **20-25 AI credits**. Treat as plan/model-dependent; verify live before making cost promises.

## REST API limitation

The FeedHive REST API key is valid for:

- `GET https://api.feedhive.com/status`
- `GET https://api.feedhive.com/socials`
- post creation/scheduling endpoints
- media upload endpoints (`POST /media/uploads`, S3 PUT, `POST /media/uploads/:id/complete`)

It did **not** expose an AI image endpoint during probes. Likely 404s included:

- `/ai/images`
- `/ai/image`
- `/ai/generate-image`
- `/ai/generateImage`
- `/ai/generate`
- `/images/generate`
- `/media/generate`
- `/posts/ai-image`

Do not assume the REST API key can generate images.

## Web-app implementation hints

FeedHive web chunks exposed GraphQL operations:

```graphql
mutation CreateAIImage($input: CreateAIImageInput!) {
  createAIImage(input: $input) {
    id
    status
    imageURL
    errorMessage
    __typename
  }
}

query GetAIImageGeneration($input: GetAIImageGenerationInput!) {
  getAIImageGeneration(input: $input) {
    id
    status
    imageURL
    errorMessage
    __typename
  }
}
```

The web modal calls:

```js
createAIImage({ prompt, aspectRatio, imageURLs })
```

and polls every ~5s while status is `PROCESSING`.

GraphQL requires a real authenticated FeedHive web/Cognito session. Unauthenticated AppSync/API-key attempts can return `Authentication required` for `createAIImage`.

## Practical workflow

1. First verify whether Hermes browser is actually logged into FeedHive. User's own browser login does not transfer to Hermes.
2. If redirected to `/get-started`, complete/skip onboarding because it can block Compose/Studio.
3. If web login fails, ask for one concrete unblock:
   - working FeedHive web credentials/session, or
   - direct image-generation key (OpenAI/FAL/Replicate), or
   - approval to use controlled SVG/HTML graphics instead.
4. For enterprise social assets, prefer: AI-generated visual base + deterministic SVG/HTML typography overlay + mobile readability QA.
