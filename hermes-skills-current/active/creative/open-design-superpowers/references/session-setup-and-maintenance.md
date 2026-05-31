# Open Design Superpowers: setup and maintenance notes

Durable workflow captured from the first Hermes/Open Design integration session.

## Local source layout

- Keep the upstream clone at `~/.hermes/vendor/open-design`.
- Keep the Hermes wrapper skill at `~/.hermes/skills/creative/open-design-superpowers/`.
- The wrapper skill should not mirror all upstream Open Design docs; it should point to the upstream clone and provide compact routing/search helpers.

## Refresh workflow

```bash
cd ~/.hermes/vendor/open-design
git pull --ff-only
python3 ~/.hermes/skills/creative/open-design-superpowers/scripts/od_catalog.py summary
python3 ~/.hermes/skills/creative/open-design-superpowers/scripts/od_catalog.py search "landing dashboard anti ai slop"
```

If upstream changes break catalog discovery, fix `scripts/od_catalog.py` rather than copying large upstream directories into the skill.

## Verification checklist

- `skill_view(name="open-design-superpowers")` succeeds.
- `hermes skills list` shows `open-design-superpowers` enabled.
- `od_catalog.py summary` reports nonzero `skills`, `design_systems`, and `craft` counts.
- `od_catalog.py show skill frontend-design` prints a valid Open Design skill.
- New Telegram/gateway sessions may need `/reset` before the newly installed skill appears in the active prompt.

## Design-task operating rule

For future design tasks, the correct lesson is not “Open Design is installed” but “route every design brief through Open Design before designing”: search catalog → read selected skill → read selected DESIGN.md → read craft references → produce artifact → visually verify → critique/fix.