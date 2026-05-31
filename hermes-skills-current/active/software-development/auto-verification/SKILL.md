---
name: auto-verification
description: Verify work with concrete evidence before claiming done. Use for fixes, deployments, code changes, automations, and workflows that need proof, not optimism.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [verification, qa, evidence, testing, delivery]
    triggers: [verify, prove it works, QA, validation, smoke test, pass/fail]
    do_not_use_for: [feature design, task routing, speculative debugging without evidence]
    compatible_workflows: [implement-review-verify-report]
---

# Auto Verification

## Purpose
Prove completion with evidence. Prefer tests, API responses, file diffs, runtime checks, screenshots, or logs over unsupported claims.

## When to Use
- After bug fixes or feature work
- Before telling the user something is complete
- For deploys, scripts, migrations, automations, or batch edits
- When work affects external behavior or user-visible output

## Do NOT Use For
- Replacing implementation planning
- Hand-waving when verification is impossible
- Browsing for its own sake without a defined success condition

## Workflow
1. Define what success means.
2. Choose the strongest available verification path.
3. Run functional checks first, then deeper data or end-to-end checks if needed.
4. Record pass/fail per checkpoint.
5. If proof is weak or incomplete, say so explicitly.

## Verification Levels
1. Functional proof — command/test exits cleanly, page/API returns expected status, artifact exists.
2. Data proof — expected content, diff, record, or output matches requirements.
3. End-to-end proof — real workflow succeeds from trigger to result.
4. Cross-surface proof — multiple environments/clients/platforms match when relevant.

## Rules
- Strong evidence beats verbal confidence.
- Prefer automated checks before manual inspection.
- Re-verify after every material change.
- If a full proof path is unavailable, provide the best available evidence and state the gap.
- Scope verification to the promised surface. If a WordPress theme/author/footer injects unrelated links or widgets into a page wrapper, do not let those unrelated defects falsely fail a targeted content/tool rewrite; verify the edited block rigorously and report unrelated findings separately.
- For SEO/indexation/canonical work, verify the exact crawl surface, not only a browser-looking page: use `allow_redirects=False` for redirects, record `X-Robots-Tag`, HTML robots meta, canonical `Link` header, HTML canonical, title, meta description, live H1 count/text, sitemap inclusion/exclusion, and cached vs cache-busted responses after purge.
- For image/content repairs on lazy-loaded pages, do not rely only on initial `document.images` or HTTP `HEAD`. Verify: placeholder strings are gone from HTML, inserted image URLs return `200 image/*`, then scroll each target image into view in a browser and confirm `complete`, `naturalWidth`, and `naturalHeight` are non-zero.
- For async jobs, backup systems, imports/exports, deploys, and queue workers, a `completed` task status is not sufficient proof. Verify the durable artifact or externally observable result: backup-list entry, remote object/file, deployment URL/version, exported record count, queue drain plus output artifact, etc. If the controller returns an error but the child job continues asynchronously, continue out-of-band polling instead of treating the controller error as final failure.
- For WordPress SEO/content cleanup, verify three distinct surfaces before calling work complete: stored post body/API state, public raw HTML, and rendered/visible page wrapper. SEO `<title>`/meta may be emitted by plugin indexables, legacy head injectors, builders, or template layers even after post title/excerpt/common custom fields are patched; report those as separate remaining platform-layer gaps instead of implying content edits failed.

## Verification Checklist
- Success criteria defined
- Checkpoints executed
- Evidence captured
- Failures or gaps stated
- Final verdict supported by proof

## Output Contract
- Artifact: verification report or checkpoint list
- Evidence: tests, outputs, statuses, screenshots, logs, or diffs
- Decision: verified / partial / failed
- Next: close, fix, or gather missing proof
