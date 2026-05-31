# Hermes configuration/control-plane repository audit pattern

Use this reference when auditing a Hermes/OpenClaw-style configuration repo, agent operating-system repo, skill library repo, or WordPress SEO/GEO/AEO automation control plane.

## Trigger

User asks to improve/audit a Hermes config repo, agent repo, skill library, SEO automation operating system, or portfolio automation control plane.

## Fast classification

Classify before work and say it briefly:

- C Repo audit
- G Multi-step implementation plan
- H Memory/context update when durable preferences/workflows emerge

For this user, prefer compact evidence-first reporting with: Outcome, Findings, Recommended Action, Implementation, Validation, Risks. For larger audits, expand only into the requested deliverables.

## Evidence-first audit sequence

1. Clone/fetch the repo shallowly unless only a few files are needed.
2. Discover local instructions first: `AGENTS.md`, `CLAUDE.md`, `.cursorrules`, `README`, `MANIFEST`, workflow files.
3. Run the repo's own validator before making claims: `make validate`, `scripts/validate.sh`, or documented equivalent.
4. Inventory architecture with counts by major directories; do not dump full file lists into chat.
5. Compare source-of-truth manifests against actual files.
6. Inspect CI for hardcoded stale checks that duplicate manifest logic.
7. Search for naming/path drift when a repo has been renamed or migrated, e.g. OpenClaw vs Hermes, `~/.openclaw` vs `~/.hermes`.
8. Check for overlapping skill trees and duplicate skill names; recommend precedence rules and validators instead of manual cleanup only.
9. Search for requested integrations by concrete names/config keys before claiming they are present or absent.
10. Produce file-level recommendations and PR-sized roadmap.

## High-signal checks

```bash
# Validate with repo tooling
make validate || bash scripts/validate.sh

# Compile Python control scripts
python3 -m compileall -q scripts core skills-approved

# Parse YAML configs/workflows
python3 - <<'PY'
from pathlib import Path
import yaml, sys
failed=[]
for p in list(Path('.').rglob('*.yml')) + list(Path('.').rglob('*.yaml')):
    if '.git' in p.parts:
        continue
    try:
        yaml.safe_load(p.read_text(encoding='utf-8-sig'))
    except Exception as e:
        failed.append(f'{p}: {e}')
if failed:
    print('\n'.join(failed)); sys.exit(1)
print('YAML parse OK')
PY

# Compare manifest paths to files
python3 - <<'PY'
from pathlib import Path
import yaml, sys
m=yaml.safe_load(open('MANIFEST.yaml', encoding='utf-8-sig'))
missing=[]
for key, value in m.items():
    if isinstance(value, list):
        for item in value:
            if isinstance(item, dict) and 'path' in item and not Path(item['path']).exists():
                missing.append(item['path'])
if missing:
    print('\n'.join(missing)); sys.exit(1)
print('manifest paths ok')
PY

# Detect duplicate skill dirs across layers
python3 - <<'PY'
from pathlib import Path
from collections import defaultdict
roots=[Path('skills'), Path('skills-approved'), Path('hermes-skills-current/active')]
seen=defaultdict(list)
for root in roots:
    if not root.exists():
        continue
    for p in root.rglob('SKILL.md'):
        seen[p.parent.name].append(str(p.parent))
for name, paths in sorted(seen.items()):
    if len(paths)>1:
        print(name, '=>', ' | '.join(paths))
PY
```

## Recommended findings to look for

- CI workflow duplicated old hardcoded checks while local validator was manifest-driven.
- Workflow uses tools not reproducible locally without setup; capture the setup or move the check into portable scripts.
- Repo branding/runtime names drift after migration.
- Huge skill snapshots cause token waste unless summarized by router/index files.
- Duplicate skills across `skills/`, `skills-approved/`, and snapshots cause ambiguous routing.
- Integration docs/templates are missing for requested MCP/browser/memory providers.
- Security docs lack MCP trust boundaries, OAuth scopes, browser automation safety, GitHub Actions permissions, and supply-chain scanning.
- Validation is structure-heavy but not behavior/config/schema-heavy.

## Preferred deliverables

- Architecture summary with inspected evidence.
- Top weaknesses prioritized by impact.
- Top improvements prioritized by implementation leverage.
- Exact file-level recommendations.
- PR roadmap with small reviewable changes.
- Validation commands.
- Security hardening checklist.
- Token-efficiency improvements.
- Final implementation sequence.

## Pitfalls

- Do not claim integration support exists just because generic docs mention MCP; search for the specific provider/config.
- Do not treat `command not found` as a durable repo flaw unless CI/local reproducibility depends on that command and docs omit setup.
- Do not propose broad rewrites when validators, routing files, and docs can produce the improvement safely.
- Do not save PR numbers, commit SHAs, or one-session progress as memory or skills.
