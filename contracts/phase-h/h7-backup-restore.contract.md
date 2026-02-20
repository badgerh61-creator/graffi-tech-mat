# Phase H.7 — Backup / Restore (Ops-Grade)

## Purpose (LOCKED)
Make the platform survivable:
- a backup can be produced on demand
- a restore can be performed deterministically
- a restore drill can be tested in CI (SQLite path)
- no immutable/audit guarantees are violated by the process

## Scope
- Backup command (safe, non-destructive)
- Restore command (explicit, guarded)
- Restore drill test for SQLite deployments
- Documentation of operator steps

## Invariants (NON-NEGOTIABLE)
1) No existing runtime code paths are changed.
2) No removal/renaming of existing models/fields/functions.
3) Restore is always explicit (must pass a confirmation flag).
4) Backup never mutates DB content.
5) Restore preserves immutable records and audit logs (by virtue of restoring the entire DB).

## Supported Backends (H.7)
- SQLite: FULL SUPPORT (file copy)
- Postgres/MySQL: STUB ONLY (must raise NotImplementedError)

## CLI Interface
python -m app.cli.ops backup --out <path>
python -m app.cli.ops restore --src <path> --confirm YES

## Exit Criteria (Freeze)
- Backup works for SQLite
- Restore works for SQLite with explicit confirmation
- CI test proves: backup -> mutate DB -> restore -> DB returns to prior state

