---
name: wordpress-backup-operations
description: Use when auditing, repairing, configuring, or verifying WordPress backup systems across MainWP, WPvivid, Google Drive/remote storage, child-site connectivity, schedules, logs, and fleet-wide backup execution.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [wordpress, backup, mainwp, wpvivid, google-drive, remote-storage, disaster-recovery]
    related_skills: [wp-rest-cloudflare, wordpress-performance-optimization, hermes-runtime-operations]
---

# WordPress Backup Operations

## Overview

Use this umbrella skill for WordPress backup infrastructure work: MainWP fleet backups, WPvivid configuration, remote storage authentication, Google Drive/S3/etc. verification, child-site connectivity, stuck backup tasks, schedule drift, and backup evidence collection.

The key rule: **do not assume remote storage OAuth is the problem just because files are missing.** Separate auth, selected destination, task creation, child-site execution, upload completion, and Drive/provider visibility.

## When to Use

- A user is trying to back up multiple WordPress sites through MainWP, WPvivid, UpdraftPlus, BlogVault, ManageWP, or similar.
- Remote storage such as Google Drive is connected but only some sites upload backups.
- MainWP dashboard shows schedules/remotes configured but backups do not appear.
- Backup jobs hang, endlessly resume, timeout, or show `no_responds`, `Unknown function`, memory exhaustion, or stale schedule state.
- The task requires proving which sites have usable restorable backups, not just clicking a backup button.

## Operating Model

1. **Inventory the fleet.** List child sites, URLs, IDs, sync/HTTP status, active backup plugin versions, MainWP Child version, and recent communication errors.
2. **Separate dashboard cache from child truth.** MainWP extension tables may be stale. Check both local MainWP cached options and live child-site responses.
3. **Verify remote auth and selected destination separately.** OAuth tokens/remote entries can exist while `remote_selected` or equivalent destination selection is empty or stale.
4. **Run one site at a time with hard timeouts.** Avoid all-sites runners until individual sites are known healthy. One broken child can block the whole fleet.
5. **Redact backup payloads aggressively.** WP backup plugins may dump OAuth tokens, refresh tokens, app passwords, signed URLs, or task payloads in debug output.
6. **Classify failure by layer.** Distinguish:
   - MainWP Child unreachable/security blocked
   - plugin/action endpoint mismatch (`Unknown function`)
   - PHP memory/execution limit failure
   - backup task stuck/no response/resumption loop
   - upload failure after local archive creation
   - provider visibility/indexing delay
7. **Tune backup workload before retrying failing sites.** Increase memory/execution where safe, reduce chunk sizes, lower per-request file/table counts, raise resume count only after reducing workload, then cancel stale tasks and retry.
8. **Verify final artifacts.** Confirm backup records on the child/site plugin and actual files in remote storage, including site prefix, timestamp, part counts, and approximate size.

## MainWP + Backuply Notes

- Backuply memory fatal errors such as `Allowed memory size of 536870912 bytes exhausted ... increase PHP memory limit` should be treated as an effective PHP runtime ceiling problem first, not as remote storage auth. Verify the new `memory_limit`, `max_execution_time`, and `WP_MAX_MEMORY_LIMIT` from inside a Backuply/wp-admin request before retrying backups.
- A small normal/MU plugin can safely harden Backuply runtime without editing Backuply itself: raise memory/time limits, call `set_time_limit()`, define WP memory constants where absent, filter `backuply_backup_self_timeout`, and ensure `wp-content/backuply/` has basic directory protections. See `references/backuply-enterprise-runtime-tuning.md`.
- If direct wp-admin automation is Cloudflare-blocked or REST app passwords lack plugin-management capability, use MainWP Child plugin install/update channels where available. When scripting MainWP internals, assign `$websites = [$website];` before calling `MainWP_Connect::fetch_urls_authed()` because the websites argument is by-reference.
- When deploying a Backuply helper/control plugin through MainWP, verify the whole chain before running backups: exact current MainWP child IDs, local-vs-served ZIP hash match, MainWP install result, then child-site helper version/endpoint response. A true MainWP package result can still install stale helper code if the served ZIP was stale. See `references/mainwp-backuply-control-plugin-deploy.md`.
- Runtime tuning is not full backup verification. Still run Backuply one site at a time and prove success by Backuply logs/artifacts/remote evidence.
- For Backuply, **log-tail success is weak evidence**. Do not declare success from `Backup Successfully Completed|success|100` alone. Strong proof requires a fresh `backuply_get_backups_info()`/backup-info artifact for the same child site URL, with a new name/timestamp, expected backup DB/files flags, size, and matching remote/location. If logs say success but no fresh artifact appears, report it as unverified or failed.
- Backuply can show stale or cross-site backup-info entries when remote folders are shared/synced. Filter backup-info records by `backup_site_url` matching the exact child domain before counting artifacts.
- A fresh same-site Backuply artifact is not necessarily `VERIFIED_FULL`: size-sanity-check it against recent full artifacts or a current file inventory, and audit excludes. If `wp-content/uploads` or broad media paths are excluded, label the result `PARTIAL-VERIFIED` / `PARTIAL_ONLY`, even if Backuply reports `backup_db=true`, `backup_dir=true`, and upload success. See `references/backuply-full-vs-partial-artifact-verification.md`.
- Validate Backuply `backuply_settings.backup_location` against keys in `backuply_remote_backup_locs` before starting/scheduling backups. If the saved location ID does not exist, Backuply may try to archive to filesystem root (e.g. `/.wp_domain_timestamp.tar.gz`) and fail with `Unable to open in write mode`. Use a valid location ID or fix the saved setting before retrying.
- If Backuply reaches archive/upload but Google Drive fails with vague provider output such as `Google Drive : 100 Continue` plus `Backup failed|error|100`, treat the log as failure unless a fresh backup-info artifact appears. Retry alternate valid remotes one at a time and verify by artifact, not by upload percentage.
- If Backuply accepts a start request but stalls at `Creating cron job`, repeated `About to call self to prevent timeout`, or an admin-ajax self-call phase, do not stack new starts. Add or use a trusted site-local helper that can directly tick Backuply's own executor (for example `backuply_backup_execute()` where available), then poll artifact state between ticks. See `references/backuply-direct-executor-recovery.md`.
- User screenshots/UI progress are not proof. A Backuply modal at 17% or 100% only means `RUNNING`/`FAILED` until a fresh same-site Backuply artifact exists. If the user shows a modal with `Backup failed`, immediately kill stale watchers/runners, extract every failing path shown in the modal, add exact excludes, reset Backuply state, redeploy/verify helper version, and rerun artifact-only.
- Backuply `Unable to writeHeader` / `Failed to write to the backup file` can be triggered by huge/generated folders during archive creation, even when the target is Google Drive. Treat paths printed immediately before the error as exclude candidates. In addition to cache and old backup folders, include optimizer/log/upload-junk paths such as `wp-content/uploads/tenweb_image_optimizer`, `wp-content/wflogs`, `wp-content/wpvivid_uploads`, and `wp-content/uploads/wpvivid_uploads` when observed. See `references/backuply-generated-folder-writeheader-failures.md`.
- For very large Backuply sites, keep the report state as `RUNNING` until artifact creation. Include the current Backuply job name, loop number, file count, archive size, and last log line. If a 9GB+ monolithic archive repeatedly fails at upload or archive traversal, switch to DB/code/config first plus separate media/chunked strategy rather than repeatedly declaring/retrying a full backup.
- When the user explicitly wants **full** backups, remove any `wp-content/uploads`/media exclusion before starting, and verify fresh artifact size against historical same-site full artifacts. A fresh DB+files artifact that is far smaller than historical size is `PARTIAL_ONLY` unless scope proof explains the delta. See `references/backuply-full-vs-partial-fleet-runs.md`.
- When the user rejects partial scope and says **only full backups for all websites**, switch to strict-full mode rather than continuing “safe exclude” runs: stop the active server-side Backuply job, clear broad exclude/skip/ignore settings, inventory `wp-content/uploads`, then rerun sequentially. In strict mode, exclude only Backuply’s static historical backup store (for example `wp-content/backuply/backups`) to prevent recursive backups; **do not exclude the whole `wp-content/backuply` / `BACKUPLY_BACKUP_DIR` tree**, because active temp archives may live under `backups-*` and excluding the root can create false `n/a` artifacts/upload failures. Mark green only as `VERIFIED_FULL` after fresh artifact + root-uploads-not-excluded + plausible size. See `references/backuply-strict-full-media-runs.md` and `references/backuply-strict-controller-tempdir-pitfall.md`.
- When the user says **all websites**, maintain an explicit fleet manifest and do not let the current active site monopolize reporting. Every domain must be either `VERIFIED_FULL`, `RUNNING_STRICT_FULL`, `QUEUED_STRICT_FULL`, `FAILED`, or `BLOCKED`; blocked sites remain in the manifest with exact blocker/next action. Legacy log-only helpers are not acceptable green proof for strict all-site full backups. See `references/backuply-all-sites-strict-fleet.md`.
- If normal plugin deployment/wp-admin is blocked but REST app-password access and Code Snippets are available, deploy the temporary strict Backuply controller as a global Code Snippets REST snippet: strip `<?php` and the plugin header, create/activate the snippet, then verify the strict route directly before starting. Treat this as an access-channel fix only; backup still requires fresh strict-full artifact proof. See `references/backuply-code-snippets-strict-controller-fallback.md`.
- If CyberPanel/resource dashboards show high CPU during Backuply repair, assume Backuply may be the active load source until proven otherwise. Check live Backuply status/log tail for archive loops and self-calls. Killing a Hermes/background watcher is not enough: Backuply may continue server-side. Stop the child-site Backuply job explicitly, verify status is empty/stopped, then report `STOPPED` only after log/status proof. See `references/backuply-cyberpanel-cpu-emergency-stop.md`.
- For urgent backup repair with a frustrated user, do not over-explain or keep handing off manual commands if an automated path exists. Prefer terse state labels (`VERIFIED_FULL`, `RUNNING`, `FAILED`, `BLOCKED`) plus the exact path/phase. Act through MainWP/helper endpoints before asking the user to paste scripts, unless credentials/access truly make automation impossible.
- Long-running Backuply watchers must survive Cloudflare `524`, blank/non-JSON executor responses, and socket timeouts without crashing; treat those as transient while the Backuply loop/file count/log tail continues to move. Persist JSONL progress and only stop on fresh artifact, explicit failure, timeout policy, or user stop. See `references/backuply-long-running-watchers.md`. Do not spam the user; report terse `RUNNING`/`VERIFIED`/`FAILED`/`STOPPED` states.
- Harden Backuply fleet runners against watcher/pass-criteria bugs: choose pass criteria based on helper capability. If same-site `backup_infos` exists, require a fresh same-site artifact; if a helper does not expose artifacts, accept `last_backup` advancing plus inactive status plus `Backup Successfully Completed` as medium-strength evidence rather than leaving a verifier stuck forever. Never confuse killing a local watcher with stopping a server-side Backuply job. See `references/backuply-fleet-runner-hardening.md`.
- For strict-full Backuply + Google Drive runs, do not mark `VERIFIED_FULL` when a fresh artifact has `size=false`/`n/a` and expected/historical full size exists; require independent remote/offsite size proof, or keep `FRESH_ARTIFACT_SIZE_UNKNOWN` / `SCOPE_NEEDS_PROOF`. If final logs contain Google Drive `100 Continue`, expired upload session, reconnect failure, or missing temp-file upload errors, state `FAILED` even if Backuply also says success. If multiple sites fail this way with clean strict scope, cut over to a server-side chunked DB/code/uploads runner instead of brute-forcing Backuply. See `references/backuply-strict-full-gdrive-failure-and-server-runner-cutover.md`.
- If CyberPanel Terminal/SSH is unavailable or blocked by 2FA, and MainWP can still install child plugins, use a temporary locked WordPress-side server backup runner instead of falling back to manual instructions. Run `mysqldump`/`tar`/`rsync` from the helper, store artifacts outside `public_html`/`uploads`, poll a status endpoint, and verify by artifact sizes/checksums. See `references/wordpress-side-server-backup-runner.md`.
- If wp-admin/REST/FTP/SSH are unavailable but CyberPanel itself is reachable, CyberPanel File Manager plus one-shot Cron Jobs can be an emergency repair channel. Use it to disable/fix MU-plugin fatals, move/delete exposed debug logs, or restore helper files; always remove the temporary cron immediately and verify the cron list is empty. See `references/cyberpanel-emergency-repair-channel.md`.
- When the user asks for **full** backups, do not accept a fresh DB+files artifact blindly. Verify root `wp-content/uploads` is not excluded and size is plausible versus historical same-site full artifacts. Exclude generated junk under uploads/cache/backup folders, but never exclude root uploads for `VERIFIED_FULL`. If a wrong-scope job is active, stop it server-side before restarting. See `references/backuply-full-media-fleet-runs.md`.
- If a full-scope Backuply run produces or logs an archive far smaller than a historical full benchmark while root uploads is **not** excluded, do not jump to either success or failure. Keep it `RUNNING_FULL` until a fresh artifact exists, then require scope proof/inventory explaining the delta before `VERIFIED_FULL`; otherwise use `SCOPE_NEEDS_PROOF` or `PARTIAL_ONLY`. Historical artifacts may include old backups/cache junk that new safe exclusions intentionally omit. See `references/backuply-scope-aware-size-sanity.md`.
- For disaster-recovery usefulness, a server-side backup is not enough if the whole VPS can be lost. Copy the verified artifacts off-server to the user-specified local/offsite folder, split huge media tarballs to avoid `413`, reassemble locally, run SHA256 verification locally, and write a restore README. See `references/wordpress-side-runner-local-download-verification.md`.
- Server-side backup is not disaster recovery until copied off-server and verified locally/remotely. For multi-GB media archives that hit web/proxy limits such as HTTP `413`, split the archive server-side (for example `split -b 100M uploads.tar uploads.tar.part-`), download parts with resume/retry, reassemble locally with `cat uploads.tar.part-* > uploads.tar`, and verify with `sha256sum -c DOWNLOAD_SHA256SUMS.txt`. Write a restore README into the destination folder. See `references/offsite-download-and-restore-verification.md`.

## MainWP + WPvivid Notes

- MainWP/WPvivid local cache can show schedules/remotes as enabled while child-site settings differ.
- In WPvivid, remote storage entries and `remote_selected` are distinct. If remote history contains a Google Drive ID but current selected remote is empty, backups may run without uploading or only some sites may upload. Repair the selected remote cache only after confirming the history entry matches the intended remote.
- `Unknown function` from MainWP/WPvivid action calls usually means the specific child-side action endpoint is unavailable/incompatible/stale, even if WPvivid itself is installed and active.
- `no_responds` plus rising `resume_count` points to a stuck child job or server-side execution failure, not a Google Drive OAuth issue.
- PHP fatal memory errors in `wpdb.php` during backup often require higher PHP memory and smaller DB/file chunks before retrying; `512M` can still be insufficient for large `wp_posts`/database dumps.
- For MainWP/WPvivid manual DB+files backups, use the UI-compatible payload value `backup_files=files+db`. A backend-only value like `all` may be accepted and may even report `completed`, but fail to create a real backup-list artifact.
- Treat `completed` task status as weak evidence. Strong proof is a new backup-list entry and, preferably, remote storage evidence (`remote=true`, matching task ID/site prefix/timestamp, and actual remote files/parts).
- A MainWP `start_backup` call can return a child reachability/error response while the child-side WPvivid task continues asynchronously. Do not stop there; poll status out-of-band by site/task before declaring failure.
- WPvivid cancel may be two-phase for no-response tasks. Normal cancel can return “force cancel?” or “will cancel after current chunk”; if the task remains active, escalate to child-side task-state cleanup rather than starting another backup on top.

## Safe Execution Pattern

- Prefer read-only audits first: site list, plugin versions, sync status, remote config, schedules, task state, logs.
- If automating starts/cancels, use per-site scripts with shell/process timeouts.
- Never print raw plugin task payloads unfiltered; sanitize `access_token`, `refresh_token`, app passwords, signed URLs, cookies, and authorization headers.
- Do not launch every backup simultaneously unless the user explicitly wants load and quota risk. Start sequentially or in tiny batches.
- For very large Backuply sites, do not brute-force one huge archive forever. First clean stale state, validate/fix remote location IDs, apply safe excludes for cache/backup/temp junk, then run artifact-only verification. If logs show Backuply traversing optimizer backup folders such as `wp-content/uploads/ShortpixelBackups/...`, stop treating the site as merely “slow”: exclude optimizer backup/cache folders before retrying. If 8–10GB+ archives still loop, upload-fail, or repeatedly stall on `wp-content/uploads`, switch to a scoped DB+code/config safety backup with `uploads` excluded and report it as `PARTIAL-VERIFIED`, not fully verified. Full media then needs a separate/chunked backup path. See `references/backuply-monolithic-media-fallback.md`.
- Preserve evidence: site ID, domain, task ID, status, last message, log name, remote file names, timestamps, sizes, and backup scope including any excluded media/uploads.
- Keep user-facing progress terse for urgent backup repair work: use `VERIFIED`, `VERIFIED_FULL`, `RUNNING`, `RUNNING_STRICT_FULL`, `FAILED`, `BLOCKED`, or `STOPPED`; avoid verbose explanation, raw route dumps, long JSON diagnostics, and never say “success” without fresh artifact proof. If raw diagnostics are needed, write them to logs/reference files and summarize only the actionable state to the user.

## Troubleshooting Matrix

- **Only one site appears in Google Drive:** Check whether other sites actually created/completed tasks; then check selected remote destination. Do not reauthorize Drive first.
- **MainWP says plugin active but backup prepare fails:** Test MainWP Child reachability and security/firewall rules for that child.
- **`Unknown function`:** Resync/reinstall/update the MainWP child-side backup integration path; verify the exact action endpoint supported by the installed WPvivid version.
- **`Too many resumption attempts`:** Cancel stale task, increase memory/execution if possible, reduce WPvivid chunk/workload settings, then retry.
- **Memory exhausted:** Raise PHP memory limit where hosted, reduce DB table/file chunk settings, and avoid high-concurrency backups.
- **Dashboard spinner hangs:** Bypass UI with backend/API scripts, but isolate per-site and redact payloads.

## Verification

Related reference: `references/backuply-gdrive-fleet.md` covers enterprise Backuply fleet backups to remote Google Drive, including selecting `pasalexios-gdrive` / `gdrive-pasalexios`, sequential execution, and evidence standards. Checklist

- [ ] Child sites inventoried with IDs/domains/status.
- [ ] Backup plugin and MainWP Child versions confirmed active.
- [ ] Remote auth checked independently from selected remote/destination.
- [ ] Stale/stuck tasks identified and either cancelled or left intentionally.
- [ ] Failed sites categorized by failure layer.
- [ ] Successful backups confirmed both in plugin status and remote storage.
- [ ] Backuply runs confirmed with fresh same-site backup-info artifacts, not log-tail success alone.
- [ ] Backuply artifact size sanity-checked against expected/historical full backups. If the fresh artifact is dramatically smaller and `wp-content/uploads` or other media paths are excluded, label it `PARTIAL-VERIFIED`, not `VERIFIED_FULL`, even when `backup_db=true` and `backup_dir=true`.
- [ ] For user-requested full backups, root `wp-content/uploads` verified absent from exclusions; generated subfolders under uploads may be excluded only when they are optimizer/cache/old-backup junk.
- [ ] For **strict only-full** requests, no broad generated/media/cache/old-backup excludes are left in Backuply settings; root `wp-content/uploads` is included; only the static Backuply backup store (for example `wp-content/backuply/backups`) is excluded, not the whole `wp-content/backuply` / active temp tree; current uploads bytes/file count captured before start; wrong-scope active jobs stopped server-side before restart.
- [ ] If a fresh artifact is much smaller than historical full size while root uploads is not excluded, a scope explanation/inventory exists before `VERIFIED_FULL`; otherwise report `SCOPE_NEEDS_PROOF` or `PARTIAL_ONLY`.
- [ ] Stale/wrong-scope Backuply jobs stopped server-side before restart; no second job stacked over an active run.
- [ ] For disaster-recovery claims, backup artifacts copied off the source server to local/offsite storage and checksum-verified.
- [ ] For disaster-recovery claims, backup artifacts copied off the source server to local/offsite storage and checksum-verified.
- [ ] For disaster-recovery claims, backup artifacts copied off the source server to local/offsite storage and checksum-verified.
- [ ] If large media archives were split for transfer, parts reassembled locally and the full archive checksum verified.
- [ ] Destination folder includes a restore README with artifact meanings, rebuild command for split parts, and restore outline.
- [ ] If a fresh artifact was produced with `wp-content/uploads` or other media paths excluded, report `PARTIAL-VERIFIED` and explicitly state media is excluded; do not call it fully fixed.
- [ ] For full disaster-recovery claims, backup artifacts copied off-server/local/offsite, huge upload archives split/reassembled if needed, local checksums verified, and a restore README placed beside the artifacts.
- [ ] Backup-info records filtered by exact child `backup_site_url` before marking a site green.
- [ ] Same-site Backuply artifacts sorted by `btime`/timestamp, not array order, before reporting latest/freshest.
- [ ] Fresh strict-full artifacts with `size=false`/`n/a` kept as `FRESH_ARTIFACT_SIZE_UNKNOWN` unless independent remote/offsite proof verifies the actual size and restoreability.
- [ ] Final Backuply tails checked for upload errors even when `Backup Successfully Completed` appears; mixed success+upload-error tails are `FAILED`, not green.
- [ ] Saved Backuply location IDs verified against configured remote location IDs before retrying failures.
- [ ] Backuply self-call/wp-cron stalls handled with direct executor ticks or split strategy; no second backup start stacked on top of a running one.
- [ ] Report labels use `VERIFIED`, `VERIFIED_FULL`, `RUNNING`, `RUNNING_STRICT_FULL`, `FAILED`, or `BLOCKED`; no “successful” wording unless a fresh same-site artifact exists.
- [ ] User-facing status is a concise manifest/label summary, not raw route dumps, raw JSON, or internal diagnostics; diagnostic detail is saved to logs/reference notes if needed.
- [ ] Report lists completed, running, failed, and blocked sites with exact next repair action.

## References

- `references/backuply-full-vs-partial-fleet-runs.md` — full-vs-partial Backuply fleet verification: size-sanity checks, uploads/media exclusion handling, `VERIFIED_FULL` criteria, and controlled full-backup helper pattern.
- `references/backuply-strict-full-media-runs.md` — strict “only full backups” pattern: stop wrong-scope jobs, clear broad excludes, exclude only Backuply self-output, inventory uploads, and require fresh plausible full artifacts.
- `references/backuply-all-sites-strict-fleet.md` — all-site strict full fleet enforcement: explicit site manifest, per-site state labels, blocked-site handling, REST/File Manager Advanced access-channel workaround, and no legacy log-only green proof.
- `references/backuply-full-media-fleet-runs.md` — full Backuply media fleet pattern: exact/root uploads exclusion detection, helper/controller workflow, safe generated exclusions, and `VERIFIED_FULL`/`PARTIAL_ONLY` labels.
- `references/backuply-scope-aware-size-sanity.md` — scope-aware size-sanity rules for unexpectedly small full-scope Backuply archives: distinguish safe generated-junk exclusions from skipped media, require fresh artifact + scope proof before `VERIFIED_FULL`.
- `references/backuply-strict-controller-tempdir-pitfall.md` — strict-full controller pitfall: exclude only static `wp-content/backuply/backups`, not the whole Backuply root/active temp tree, to avoid false `n/a` artifacts and upload-missing-file failures.
- `references/backuply-code-snippets-strict-controller-fallback.md` — fallback for deploying a temporary strict Backuply controller through Code Snippets REST when wp-admin/plugin upload/CyberPanel is blocked; includes snippet conversion, route verification, parallel runner, and no-raw-diagnostics reporting discipline.
- `references/mainwp-backuply-control-plugin-deploy.md` — MainWP helper/control-plugin deployment verification chain: exact child IDs, served ZIP hash, child helper version check, Backuply prep/start ordering, and urgent terse reporting.
- `references/backuply-optimizer-backup-bloat.md` — Backuply huge-site pitfall where optimizer backup folders such as ShortPixel backups bloat archives; includes safe exclude/reset/rerun pattern and terse reporting states.
- `references/backuply-long-running-watchers.md` — no-crash watcher pattern for huge Backuply jobs behind Cloudflare: tolerate 524/timeouts/blank responses, persist JSONL progress, honor user stop, and use terse artifact-only reporting.
- `references/backuply-fleet-runner-hardening.md` — multi-site Backuply/GDrive runner criteria: sequential execution, remote-ID validation, JSONL progress, helper-capability-aware pass criteria, stuck-watcher recovery, and terse VERIFIED/RUNNING/FAILED/BLOCKED reporting.
- `references/backuply-enterprise-artifact-runs.md` — concise enterprise pattern for huge Backuply site runs: stale-state cleanup, safe excludes, direct executor ticks, artifact-only pass criteria, and terse VERIFIED/RUNNING/FAILED/BLOCKED reporting.
- `references/backuply-direct-executor-recovery.md` — Backuply direct-executor recovery pattern for wp-cron/admin-ajax stalls, invalid location repair, artifact-only verification, huge archive handling, and blunt VERIFIED/RUNNING/FAILED/BLOCKED reporting.
- `references/backuply-artifact-verification.md` — Backuply-specific artifact verification rules: fresh same-site backup-info records, invalid location-ID failure mode, Google Drive upload false positives, and reporting states.
- `references/backuply-generated-folder-writeheader-failures.md` — Backuply UI/log failure pattern where generated folders such as TenWeb optimizer, Wordfence logs, WPvivid uploads, or ShortPixel backups trigger `Unable to writeHeader`; includes exact-exclude/reset/rerun procedure and terse state labels.
- `references/backuply-monolithic-media-fallback.md` — fallback pattern for Backuply jobs that still stall on huge `wp-content/uploads`: scoped DB+code/config artifact, `PARTIAL-VERIFIED` reporting, and separate media backup strategy.
- `references/mainwp-wpvivid-google-drive-triage.md` — session-derived triage pattern for MainWP + WPvivid + Google Drive where only one child site uploaded successfully.
- `references/backuply-cyberpanel-cpu-emergency-stop.md` — emergency pattern for CyberPanel CPU spikes caused by Backuply archive loops: stop local runner, verify/stop server-side job, and switch to DB/code first plus separate media strategy.
- `references/offsite-download-and-restore-verification.md` — disaster-recovery handoff pattern for copying server-side backups offsite/local, splitting multi-GB media archives around HTTP/proxy limits, reassembling locally, checksum verification, and writing a restore README.
- `references/wordpress-side-runner-local-download-verification.md` — WordPress-side helper pattern for DB/code/uploads backup plus local/offsite download: handle `413` with split parts, `524` as indeterminate while server work may continue, origin `--resolve` bypass when appropriate, local reassembly, SHA256 verification, and restore README.
- `references/mainwp-wpvivid-enterprise-repair-notes.md` — enterprise repair notes: redacted per-site orchestration, `files+db` payload pitfall, async verification, stuck-task handling, and memory-fatal mitigation.
