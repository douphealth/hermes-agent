# NeuronWriter ↔ WordPress bridge notes

Use this when optimizing an existing WordPress post with NeuronWriter before publishing.

## Durable workflow

1. Open the correct NeuronWriter project and query, then immediately capture and report the direct editor URL (`https://app.neuronwriter.com/analysis/view/...`) if the user may need to find it manually.
2. Treat local rewrite artifacts (`optimized-article.html`, `.txt`, backups) as agent-side drafts only. They are not visible to the user in NeuronWriter or WordPress until pasted/imported or published.
3. If the NeuronWriter API key fails or is inactive but browser login works, continue through the browser UI rather than blocking; report the API gap separately without claiming the tool is unusable.
4. Paste/import the draft into NeuronWriter and tune until the visible score target is met. Capture score evidence from the editor before publishing.
5. Only after final grammar cleanup and score verification, publish to WordPress via the normal WordPress pipeline and verify the public URL.

## User-facing reporting rule

When the user asks "where is the post?" or asks for a URL, give the exact clickable surface first:

- NeuronWriter editor URL if they mean optimizer workspace.
- Public WordPress URL if they mean the live article.
- State explicitly whether the rewritten draft has been pasted to NeuronWriter and/or published to WordPress.

Do not lead with filesystem paths unless the user explicitly asks for artifacts/files.