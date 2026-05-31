# Upstreaming SEO/GEO/AEO superpowers into Hermes Agent

Use this when converting a locally installed SEO/GEO/AEO skill into a portable Hermes Agent repository update.

## Durable workflow

1. Keep third-party repositories out of the Hermes source tree.
   - Local installs belong under `~/.hermes/vendor/`.
   - Repo additions should be skill instructions, references, templates, and deterministic wrapper scripts only.
2. Add the skill under the repository's optional skills tree, not the live profile tree:
   - `optional-skills/devops/codex-seo-superpowers/SKILL.md`
   - `optional-skills/devops/codex-seo-superpowers/references/`
   - `optional-skills/devops/codex-seo-superpowers/templates/`
   - `optional-skills/devops/codex-seo-superpowers/scripts/`
3. Regenerate website docs/catalog/sidebar after adding the optional skill.
   - Use the repo's docs generation script when available.
   - Revert unrelated regenerated skill pages if the generator refreshes stale docs from other skills.
4. Validate before commit:
   - `python3 -m py_compile optional-skills/devops/codex-seo-superpowers/scripts/hermes_codex_seo_runner.py`
   - Runner smoke test against `https://example.com` with a temporary output directory.
   - `git diff --check`
   - Relevant pytest slice for prompt builder, skill usage, packaging metadata, and toolset distributions.
   - Secret-pattern scan of the staged diff before committing.
5. If direct push to the upstream repository is denied:
   - Push the branch to the user's fork.
   - Open an upstream PR from `user:branch` to `upstream:main`.
   - If pushing with an embedded temporary token URL, immediately remove token-bearing branch upstream config and replace it with a clean named remote.

## Pitfalls

- Do not commit vendored third-party repositories or local virtualenvs.
- Do not leave token-bearing HTTPS URLs in `.git/config` branch upstream settings.
- Do not claim upstream is updated if only a fork was updated; distinguish fork push from upstream PR.
- Do not preserve unrelated generated-doc churn unless it is necessary for the skill being upstreamed.

## Evidence to report

- Branch name and commit SHA.
- Fork URL and upstream PR URL if applicable.
- Exact validation commands and pass counts.
- Whether direct upstream push succeeded or was permission-denied.
