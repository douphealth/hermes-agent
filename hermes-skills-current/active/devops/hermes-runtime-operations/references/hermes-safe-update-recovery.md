# Hermes Safe Update and Runtime Recovery

Use this reference when updating Hermes Agent itself, especially from a Telegram/gateway session where the running process may restart mid-turn.

## Success Criteria

- Repo is at latest `origin/main` with `git rev-list --left-right --count HEAD...origin/main` returning `0\t0`.
- `hermes --version` says `Up to date`.
- Working tree is clean unless the user explicitly wants local custom patches reapplied.
- Gateway is running on the updated venv entry point.
- Config has been migrated and `hermes doctor` has no unexpected new blockers.
- Focused smoke tests pass for any touched or historically fragile areas.

## Safe Update Workflow

1. **Snapshot before touching anything.** Record version, branch, HEAD, origin URL, `git status --short`, unstaged diff, staged diff, and untracked files into `~/.hermes/backups/hermes-update-<UTC_TS>/`.
2. **Preserve local edits.** Use `git stash push -u -m pre-hermes-update-<UTC_TS>`. If ignored or problematic untracked directories remain, move them into the backup directory before updating.
3. **Run the update.** Execute `hermes update` from `~/.hermes/hermes-agent`. If the gateway restarts and interrupts the tool call, resume by checking git/version state rather than rerunning blindly.
4. **Verify upstream state.** Check:
   - `hermes --version`
   - `git rev-parse --short HEAD`
   - `git rev-parse --short origin/main`
   - `git rev-list --left-right --count HEAD...origin/main`
   - `git status --short`
5. **Run migration/health checks.** Run `hermes config check` and `hermes doctor --fix` when config version or WAL warnings appear.
6. **Smoke test.** Run focused tests around the changed/touched areas, e.g. `./venv/bin/python -m pytest tests/tools/test_delegate.py tests/agent/test_unsupported_temperature_retry.py -q -o 'addopts='` when delegation or provider retry behavior is relevant.
7. **Verify gateway.** `hermes gateway status` should show the user service active and running from the updated `venv/bin/python -m hermes_cli.main gateway run --replace` command.
8. **Report preserved customizations.** If local custom source patches were stashed but not reapplied, say that explicitly and provide the stash/backup handle.

## Common Recovery Patterns

### Update tool call interrupted by gateway restart

Treat the interruption as expected. Do not assume failure. Resume with version/git checks:

```bash
hermes --version
git rev-parse --short HEAD
git rev-parse --short origin/main
git rev-list --left-right --count HEAD...origin/main
git status --short
```

If HEAD equals origin/main and behind/ahead is `0\t0`, the update completed even if the prior tool returned exit 130.

### Large state.db WAL after update

If `hermes doctor` reports a large WAL and `doctor --fix` does not shrink it, run a direct SQLite checkpoint using Python stdlib:

```bash
python3 - <<'PY'
import os, sqlite3
p=os.path.expanduser('~/.hermes/state.db')
wal=p+'-wal'
print('wal_before', os.path.getsize(wal) if os.path.exists(wal) else 0)
con=sqlite3.connect(p, timeout=10)
print('checkpoint', con.execute('PRAGMA wal_checkpoint(TRUNCATE)').fetchall())
con.close()
print('wal_after', os.path.getsize(wal) if os.path.exists(wal) else 0)
PY
```

This captures the fix pattern, not a durable claim that WAL is always broken.

### Corrupted Kanban DB after update

If gateway logs say `kanban.db is not a valid SQLite database`, verify with Python `sqlite3` rather than relying on the `sqlite3` shell being installed. Preserve the corrupt file before reinitializing:

```bash
DB="$HOME/.hermes/kanban.db"
BACKUP_DIR="$HOME/.hermes/backups/hermes-update-$(date -u +%Y%m%dT%H%M%SZ)"
mkdir -p "$BACKUP_DIR"
[ -e "$DB" ] && mv "$DB" "$BACKUP_DIR/kanban.db.corrupt.$(date -u +%Y%m%dT%H%M%SZ)"
hermes kanban init
python3 - <<'PY'
import os, sqlite3
p=os.path.expanduser('~/.hermes/kanban.db')
con=sqlite3.connect(p)
print('integrity', con.execute('pragma integrity_check').fetchone()[0])
print('tables', len(con.execute("select name from sqlite_master where type='table'").fetchall()))
PY
```

Do not encode this as “Kanban is broken”; it is only a recovery path for invalid DB files.

## Pitfalls

- Do not discard local source edits; stash and separately back them up before update.
- Do not reapply custom patches automatically after updating unless the user asks; a clean upstream tree is often the goal.
- Do not treat `hermes update` interruption during a gateway restart as a failed update until git/version checks prove it.
- Do not report “done” from version alone; verify git parity, clean tree, gateway status, config migration, and focused tests.
