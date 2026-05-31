# NeuronWriter + WordPress rewrite pipeline

Use this reference when optimizing an existing WordPress article with NeuronWriter and publishing the rewrite.

## Trigger
- User asks to rewrite/update an existing WordPress post and explicitly wants a NeuronWriter score target before publishing.
- Especially relevant for affiliate/SEO/GEO/AEO pages where exaggerated metrics must be removed and claims must be source-backed.

## Durable workflow
1. **Backup first**
   - Save the public HTML, WordPress API/XML-RPC post JSON, and raw stored post HTML before editing.
   - Record post ID, canonical URL, current title, status, and byte/word counts in the workdir.
2. **Access NeuronWriter carefully**
   - Retrieve credentials/API keys only from the local secret source at runtime; never echo or persist secrets in outputs.
   - If the NeuronWriter API key returns unauthorized/inactive but browser login works, continue with browser/editor workflow rather than claiming NeuronWriter is unavailable.
3. **Capture baseline evidence**
   - Open the existing project/query, capture baseline content score, suggested word target, and visible recommended terms/entities.
   - Save extracted terms/entities locally as evidence for tuning.
4. **Rewrite for trust before tuning**
   - Remove unsupported/exaggerated metrics, guaranteed ranking claims, fake conversion/ranking numbers, and hype language.
   - Add source-backed process sections using primary documentation where possible: Google Search Central helpful content, SEO starter guide, title links, snippets, crawlable links, image SEO, structured data, and Schema.org when relevant.
   - Add contextual internal links to relevant hubs and next-step pages; avoid random PageRank-only links.
5. **Tune terms without damaging prose**
   - Use NeuronWriter terms/entities as coverage targets, not as permission to keyword-stuff.
   - After every term-count tuning pass, do a human grammar/readability cleanup. Watch for awkward exact-match artifacts like duplicated nouns, wrong articles, or unnatural phrases created solely to satisfy terms.
6. **Do not publish prematurely**
   - Do not publish while the draft still has grammar artifacts or while the requested NeuronWriter score is unverified.
   - If the user asked for >90, final publish requires a verified NeuronWriter score of 90+ or an explicit user override.
7. **Publish and verify**
   - Publish via the site’s safest available path, then purge/refresh cache if applicable.
   - Verify public URL: HTTP 200, indexable, canonical correct, one visible H1, clean title/meta, no raw CSS/schema leaks, new sections visible, internal/external links resolve, and no unsupported metrics remain.

## Reporting standard
- Report only verified facts: baseline score, final NeuronWriter score, post ID, live URL, publish status, and QA checks.
- If tool-call or access limits prevent completion, explicitly say what is not done; never imply the post was published or scored >90 without evidence.

## Pitfalls
- NeuronWriter exact-term optimization can make prose worse. Always run a final readability pass after term tuning.
- A working browser login and failing API key is not a blocker for manual/browser-based scoring.
- Publishing before NeuronWriter score verification violates score-target tasks and creates avoidable rollback risk.
