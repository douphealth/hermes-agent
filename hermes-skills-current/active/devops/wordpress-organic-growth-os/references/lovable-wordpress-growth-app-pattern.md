# Lovable front-end for WordPress Organic Growth OS

Use when the user asks to make a Lovable app dramatically more helpful for WordPress website changes, organic traffic, SEO/GEO/AEO, SERP rankings, or AI visibility.

## Target UX pattern

The app should not be a generic dashboard. It should be a practical command center that answers immediately:

> What should I fix today to grow traffic safely?

Core sections to request from Lovable:

1. Command Center — portfolio health, organic growth, AI visibility, technical risk, content opportunity, monetization readiness, and top actions.
2. WordPress Manager — site URL, REST/XML-RPC/sitemap/Yoast/cache status, read-only vs edit mode, backups, changelog, rollback.
3. SEO/GEO/AEO Audit Engine — technical, on-page, content quality, AEO, GEO, AI crawler visibility, schema, internal links, E-E-A-T, monetization.
4. WordPress Change Studio — workflows for title/meta/H1 drift, post refreshes, FAQ/AEO blocks, GEO/AI blocks, internal links, schema, redirects, shortcode/template residue, affiliate disclosure/CTA.
5. AI Visibility Lab — llms.txt readiness, robots AI crawler access, entity clarity, answer extraction, quotable paragraphs, citation likelihood, crawler allow/block summary.
6. Content Refresh Queue — URL, title, H1, age, intent, decay risk, refresh type, priority.
7. Topical Authority Map — pillars, supporting pages, missing cluster pages, cannibalization, internal link gaps.
8. Fix Draft Builder — Yoast metadata, outlines, direct answers, FAQs, schema suggestions, internal link placements, redirects, Gutenberg/HTML blocks, changelog text.
9. Safety / Verification Center — backup required, public verification, status code, canonical, robots, H1 count, title/meta, schema parse, raw shortcode leakage, before/after diff, rollback.

## Prompting standard

- Demand a premium command-center UI, not just cards.
- Require clear primary actions on every screen.
- No fake metrics: use “Connect data” / “Needs verification” when GSC/GA4/ranking data is missing.
- Every recommendation must include evidence, impact, risk, effort, and exact action.
- Include realistic sample sites and issues when backend integrations are not wired yet, clearly labeled as sample/mock.
- Ask Lovable for reusable components: SiteHealthCard, ScoreRing, PriorityActionCard, IssueTable, FixWorkflowStepper, URLAuditDrawer, ChangePreviewDiff, SafetyChecklist, AIVisibilityPanel, TopicalMapCards, ContentRefreshQueue, WordPressConnectorCard, EvidenceBadge, ImpactRiskEffortMatrix.

## Safety requirements to include

- Read-only mode vs edit mode.
- Never display secret values.
- Backup before production edits.
- Diff preview before apply.
- Verify public URL after apply.
- Save changelog and rollback path.

## If Lovable automation is blocked

If Lovable project chat API returns `captcha_required`, do not claim submission. Save the prompt artifact, give the project URL and exact next step to paste/submit it manually, then QA/iterate after the user completes CAPTCHA.
