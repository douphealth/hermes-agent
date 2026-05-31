# REST Execution Checklist

## Access / Preflight
- verify REST auth
- identify object ID and type
- inspect trust-page slugs
- inspect SEO plugin / schema layer
- fetch current object with context=edit
- save backup JSON to /tmp

## Build Payload
- title / excerpt aligned to intent
- content.raw updated
- HTML wrapped in `<!-- wp:html -->` when needed
- trust note included if required
- quick-answer / intent note included if required
- related-guides block included
- next-step CTA included
- internal links mapped
- duplicate-H1 risk checked

## Write
- use POST + X-HTTP-Method-Override: PUT if needed
- browser-like UA
- file-based payload for large content

## Verify
- REST object updated
- public URL 200
- cache-busted URL 200
- exactly one H1 live
- blocks render correctly
- internal/trust links live
- schema checked if relevant
- title/meta/og checked separately
- plain URL vs cache-busted output compared

## Report
- body-layer success
- head-layer success or blocker
- cache/plugin blocker notes
- next recommended pages in batch
