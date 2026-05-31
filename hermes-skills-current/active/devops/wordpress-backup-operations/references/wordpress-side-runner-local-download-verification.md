# WordPress-side server backup runner: local download + verification

Use this when CyberPanel/SSH/terminal is blocked (2FA/no terminal), PHP backup plugins are unsafe for huge sites, but MainWP can still install a locked helper plugin on the child site.

## Pattern

1. Deploy a temporary locked child-site helper through MainWP.
2. Run server-level backups from the helper, storing outside `public_html` and outside `wp-content/uploads` to avoid recursive copy:
   - `mysqldump --single-transaction --quick --skip-lock-tables --no-tablespaces` piped to `gzip -1`
   - `tar` for code/config excluding `wp-content/uploads`, cache, backup, logs, and optimizer junk
   - `rsync -aH` for `wp-content/uploads/`
3. Verify server-side artifacts by size and SHA256 before claiming success.
4. Add package/download endpoints only after backup is verified.
5. Download DB/code/checksum files directly; package uploads as `uploads.tar` and split into small chunks before transfer.
6. Reassemble `uploads.tar` locally and run checksum verification locally.
7. Write a `RESTORE_README.txt` into the local backup folder.

## Critical implementation details

- Use `bash -o pipefail` around `mysqldump | gzip`, otherwise an empty 20-byte gzip can hide a failed dump.
- Pass DB password via `MYSQL_PWD=[REDACTED] or safe environment handling; avoid relying on an exposed `-pPASSWORD` where logs may leak it.
- Split `DB_HOST` values like `localhost:3306` into host + port for `mysqldump`/`mysql`.
- Store generated backup folders outside uploads, e.g. `/home/<site>/hermes-enterprise-backups/<stamp>`, not under `wp-content/uploads`, or media copy can recurse into the backup itself.
- HTTP download of multi-GB artifacts can fail with `413`; split large media tarballs server-side, e.g. `split -b 100M uploads.tar uploads.tar.part-`.
- If Cloudflare/proxy causes `524`, `403`, stale helper versions, or cached apex responses, try the canonical host (`www` vs apex) and, when an origin IP is known, use direct-origin `curl --resolve host:443:ORIGIN_IP` for package/download requests.
- Treat a long packaging request that ends in `524` as indeterminate: poll status/metadata afterward because the server-side tar/split may have continued and completed.
- Keep split parts even after assembling `uploads.tar`; they are useful for transfer safety and rebuilding.

## Local verification checklist

In the target Windows folder (WSL path translated from `D:\...`):

```bash
# after all parts are downloaded
cat uploads.tar.part-* > uploads.tar
sha256sum -c DOWNLOAD_SHA256SUMS.txt > VERIFY_RESULT.txt 2>&1
```

Pass criteria:

- `database.sql.gz: OK`
- `code_config.tar.gz: OK`
- `uploads.tar: OK`
- every `uploads.tar.part-*`: `OK`
- report/checksum files: `OK`
- `sha256sum` exit code `0`
- `RESTORE_README.txt` present with extraction/import instructions

## User-facing reporting

For urgent recovery work, report terse states and exact local paths:

- `RUNNING`: include current phase and bytes/part progress.
- `VERIFIED_FULL`: only after local checksum pass.
- `FAILED/BLOCKED`: include exact failing layer (`2FA`, `413`, `524`, stale route, DB dump, checksum). Do not call a server-side backup sufficient until it has been copied off-server or explicitly state it is not offsite-safe.
