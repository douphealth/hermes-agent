# Backuply Scope-Aware Size Sanity

Use when a Backuply job was prepared for “full” scope (DB + files, root `wp-content/uploads` not excluded) but the resulting/logged archive size is much smaller than a historical full benchmark.

## Lesson

A dramatic size delta is not automatically proof of failure when the new run intentionally excludes generated junk such as old backup archives, caches, optimizer backups, or temporary folders. However, it is also not automatically `VERIFIED_FULL`. Treat the run as `RUNNING_FULL` until a fresh same-site artifact exists, then require scope evidence that explains the delta.

## Verification pattern

1. Before start, snapshot:
   - fresh same-site artifact count/timestamps;
   - selected remote/location ID;
   - DB/files flags;
   - exclusions, with exact/root `wp-content/uploads` detection only;
   - historical same-site full artifact size if available.
2. During upload/archive, report only `RUNNING_FULL` with archive size/upload progress. Do not infer final scope from an in-progress tar size.
3. After completion, verify a fresh same-site backup-info artifact appears on the intended remote.
4. If artifact size is far below historical full size, collect a scope explanation before `VERIFIED_FULL`:
   - root uploads not excluded;
   - safe generated exclusions list contains old backup/cache/temp folders;
   - Backuply file count/log tail shows traversal beyond DB/code and into media where possible;
   - optional current server inventory (`du`/helper inventory) separates user media from generated/old backup bloat.
5. Status labels:
   - `VERIFIED_FULL` only when fresh artifact + full-scope config + plausible size or documented delta explanation exist.
   - `SCOPE_NEEDS_PROOF` when fresh artifact exists but size is unexpectedly small and no inventory/log proof explains it.
   - `PARTIAL_ONLY` when root uploads/media is excluded or file-selection settings prove media was skipped.

## Reporting style

Keep user updates terse: `RUNNING_FULL`, `VERIFIED_FULL`, `SCOPE_NEEDS_PROOF`, `PARTIAL_ONLY`, `FAILED`, or `BLOCKED`, followed by exact evidence (artifact timestamp/size, root uploads exclusion state, historical benchmark, and one-line next action).