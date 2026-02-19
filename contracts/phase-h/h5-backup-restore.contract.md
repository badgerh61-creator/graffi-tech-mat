# Phase H.5 — Backup / Restore (Ops-Grade)

## Purpose (LOCKED)
Make the system recoverable: provide a testable backup + restore procedure
that preserves immutability and audit integrity.

## Scope
- Database backup and restore commands (ops runnable)
- Optional admin endpoints to trigger backup/restore (disabled by default)
- Tests that verify round-trip restore works for critical invariants

## Invariants (NON-NEGOTIABLE)
1) No schema changes required for H.5
2) No deletion or renaming of existing code paths
3) Restore MUST preserve:
   - immutable snapshots
   - audit logs
   - jobs (including Job.state + Job.status compatibility)
4) Restore procedure must be idempotent at file level (same backup file can be restored to an empty DB)
5) Backups are restricted to trusted operators (CLI), or admin-only endpoints when enabled

## Deliverables
- backup service with:
  - create_backup(path) -> metadata
  - restore_backup(path) -> metadata
- storage format:
  - JSON lines or single JSON object
  - includes table name + rows
- tests:
  - round-trip: seed -> backup -> wipe -> restore -> verify invariants
  - restore does not mutate existing rows unexpectedly (in empty-db restore case)

## Exit Criteria
- `create_backup` produces a file
- `restore_backup` restores into a clean DB
- tests pass deterministically in CI

