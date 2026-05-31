# Offsite Download and Restore Verification for Large WordPress Backups

Use this when a server-side WordPress backup has been created but the user needs practical disaster recovery: an off-server copy they can restore if the VPS is lost.

## Lessons

- A backup stored only under the same hosting account/server is not disaster recovery. It is useful for local rollback but is lost with the server.
- Always identify and deliver the concrete restore artifacts:
  - `database.sql.gz` — MySQL dump
  - `code_config.tar.gz` — WordPress code/plugins/themes/config, excluding uploads
  - `uploads.tar` or equivalent split parts — `wp-content/uploads`
  - checksum files and a restore README
- Do not tell the user a backup is “safe” until an offsite/local copy has been downloaded and checksum-verified.

## Large-file download pattern behind Cloudflare / web servers

If a multi-GB archive download fails with HTTP `413`, `524`, gateway timeout, or similar:

1. Keep DB/code artifacts separate; download them normally.
2. Server-side package media into a plain tar if needed:
   ```bash
   cd /path/to/backup && tar --warning=no-file-changed --ignore-failed-read -cf uploads.tar uploads
   ```
3. Split the large tar into web-download-safe chunks:
   ```bash
   cd /path/to/backup && split -b 100M uploads.tar uploads.tar.part-
   ```
4. Generate checksums for both the whole tar and all parts:
   ```bash
   sha256sum database.sql.gz code_config.tar.gz uploads.tar uploads.tar.part-* REPORT.txt SHA256SUMS.txt SHA256SUMS.uploads.txt > DOWNLOAD_SHA256SUMS.txt
   ```
5. Download parts with resume/retry:
   ```bash
   curl -L --fail --retry 5 --continue-at - -o uploads.tar.part-aa 'https://...'
   ```
6. Reassemble locally:
   ```bash
   cat uploads.tar.part-* > uploads.tar
   ```
7. Verify locally:
   ```bash
   sha256sum -c DOWNLOAD_SHA256SUMS.txt
   ```

Only after this passes should the local/offsite copy be reported as `VERIFIED`.

## Restore README contents

Write a short `RESTORE_README.txt` into the downloaded folder with:

- exact local path
- meaning of each artifact
- checksum command already used
- how to rebuild `uploads.tar` from parts
- restore outline:
  ```bash
  tar -xzf code_config.tar.gz -C /home/DOMAIN/public_html
  tar -xf uploads.tar -C /home/DOMAIN/public_html/wp-content
  gzip -dc database.sql.gz | mysql -u DB_USER -p DB_NAME
  chown -R DOMAIN:DOMAIN /home/DOMAIN
  find /home/DOMAIN/public_html -type d -exec chmod 755 {} \;
  find /home/DOMAIN/public_html -type f -exec chmod 644 {} \;
  ```

## Reporting style for urgent users

Use terse states and concrete evidence:

- `LOCAL COPY = VERIFIED`
- exact Windows and WSL paths
- artifact sizes
- checksum result
- if split/reassembled, explicitly say why and that the final tar checksum passed

Avoid long reassurance without restoreability facts.