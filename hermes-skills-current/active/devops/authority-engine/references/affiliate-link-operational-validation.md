# Affiliate Link Operational Validation

Use this when the user provides a list of affiliate/referral links and asks for precise confirmation that they are valid, operational, and usable as a monetization base.

## Goal
Produce a sanitized master table that separates:
- `USE NOW` — public link resolves and tracking/referral evidence is acceptable.
- `VERIFY MANUALLY BEFORE USE` — link resolves but bot protection, brand migration, dashboard ambiguity, or invite/referral uncertainty exists.
- `RETRIEVE FROM DASHBOARD` — no public affiliate link was supplied; dashboard/login data alone is not publishable.
- `DO NOT USE` — broken, inactive, wrong merchant, 404, closed merchant, or account-state error.

## Safety and privacy
- Never preserve or output usernames, passwords, API keys, dashboard credentials, or raw secret values.
- Build a sanitized inventory containing only: program, category, link type, public affiliate/referral URL, expected domain(s), and expected tracking marker(s).
- If credentials are needed for dashboard confirmation, retrieve them only from the approved local secret source and redact values in all outputs.

## Efficient validation workflow
1. Normalize public links:
   - Add `https://` to bare `www.` links.
   - Correct obviously malformed pasted schemes only when the intended public link is clear (`http:/` → `http://`, `https:/` → `https://`).
   - Keep dashboard/login URLs separate; do not treat them as publishable affiliate links.
2. For each public affiliate/referral URL, run a browser-like GET with redirects enabled. HEAD is not enough; many affiliate networks block or behave differently on HEAD.
3. Capture:
   - original URL
   - HTTP status
   - full redirect chain
   - final URL
   - expected-domain match
   - tracking/referral marker survival where visible (`via=`, `fpr=`, `ref=`, `id=`, `bta=`, `u=`, `m=`, `kaid=`, etc.)
   - short evidence note
4. Inspect the final body/title for network error pages, not just HTTP 200. Some broken affiliate links return 200 with error content.
5. Assign a strategy status using the taxonomy above.
6. Export at least CSV/XLSX/Markdown with conditional statuses and no credentials.

## Network-specific red flags
- ShareASale/Awin:
  - `awin1.com/closedMerchant.html` or body text like `This link is inactive` = `DO NOT USE`, even if status is 200 and original ShareASale parameters are present.
  - Preserve `u=` and `m=` evidence, but do not mark as approved if the merchant is closed/inactive.
- ClickBank:
  - `hop-apps.clickbank.net` with `errCode=accntstate` = `DO NOT USE`; the hop link/account state must be repaired before publishing.
  - A visible `tid=` marker alone is not enough if the final destination is an error page.
- PartnerStack / FirstPromoter / Rewardful / Tapfiliate / Impact:
  - If a tracking marker survives and the final page is the merchant/pricing/signup page, usually `USE NOW`.
  - If the final brand/domain changed, mark `VERIFY MANUALLY BEFORE USE` unless the dashboard confirms the migration.
- 403/Cloudflare/bot protection:
  - If redirect chain preserves affiliate markers and reaches the expected merchant before a 403, mark `VERIFY MANUALLY BEFORE USE`, not automatically broken.
  - Ask for or perform dashboard click verification if the user needs commission-grade certainty.
- Invite/org links:
  - Public invite links that resolve but do not prove commissions should be `VERIFY MANUALLY BEFORE USE`, not affiliate-approved.
- Wrong merchant/mismatched program:
  - If the program is HubSpot but the URL is ConvertKit/mbsy and returns 404 or routes to another merchant, mark `DO NOT USE`.

## Dashboard-side confirmation for “1000% operational”
Public checks prove resolve/redirect/tracking evidence. Commission-grade certainty requires dashboard-side confirmation:
1. Open the link in a clean browser/profile.
2. Confirm the click registers in the affiliate dashboard.
3. Confirm campaign/source/subID attribution where available.
4. Confirm the merchant/program is active and commissionable.
5. Only then lock the link into sitewide monetization modules.

## Output standard
Return concise counts plus files:
- `USE NOW` count
- `VERIFY MANUALLY BEFORE USE` count
- `RETRIEVE FROM DASHBOARD` count
- `DO NOT USE` count
- explicit `DO NOT USE` list with reason
- explicit manual-verification list with reason
- downloadable master table, preferably XLSX + CSV + Markdown

Avoid large inline tables in chat/Telegram; attach the file and summarize bullets.
