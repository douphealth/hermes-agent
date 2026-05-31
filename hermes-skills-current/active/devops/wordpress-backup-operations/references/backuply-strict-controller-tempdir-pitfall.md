# Backuply strict controller temp-dir exclusion pitfall

## Trigger

Use this note when forcing Backuply into strict/full mode by clearing broad excludes and allowing only Backuply self-output exclusions.

## Lesson

Do **not** blindly exclude `BACKUPLY_BACKUP_DIR` or the whole `wp-content/backuply` tree.

On some Backuply installs, the active archive temp/work directory is under a sibling like:

- `wp-content/backuply/backups-*/tmp/<backup_name>/...`

If the strict controller excludes the root Backuply directory (`wp-content/backuply`), Backuply can lose or skip its own temp files during archive finalization/upload and produce misleading output such as:

- missing `softperms.txt`, `softver.txt`, or `<backup_name>.php`
- `Upload Failed! Because the file is not present on the server`
- `Archive created with a file size of n/a`
- a fresh artifact with `size=false` / `0`, even after many files were added
- contradictory log tail containing both `Backup failed` and `Backup Successfully Completed`

## Correct strict-full exclusion rule

For strict full-media runs, exclude only the static historical Backuply backup store to avoid recursive backups, for example:

```text
/wp-content/backuply/backups
```

Do **not** exclude:

```text
/wp-content/backuply
/wp-content/backuply/backups-* 
/wp-content/uploads
```

## Validation checklist before starting the rerun

1. Stop any active server-side Backuply job; killing a local watcher is not enough.
2. Deploy/update the controller.
3. Call the controller `prepare` endpoint.
4. Verify `exclude`, `exclude_files`, and `exclude_folders` contain only the static Backuply backup store path.
5. Verify root `wp-content/uploads` is not excluded.
6. Inventory `wp-content/uploads` bytes/files before start.
7. Start the backup and mark green only after fresh same-site artifact proof + no failure tail + plausible size/scope evidence.

## Reporting rule

If this pitfall is discovered mid-run, tell the user concisely:

- the prior strict rule was wrong,
- the server-side job was stopped,
- the controller was updated,
- prep was verified on the fleet,
- new runs were restarted.

Do not paste raw route dumps or JSON unless explicitly requested.
