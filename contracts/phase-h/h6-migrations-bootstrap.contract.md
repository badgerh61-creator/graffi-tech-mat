# Phase H.6 — Migrations + Bootstrap (Ops-Grade)

## Purpose (LOCKED)
Ensure the system can be:
1) installed from zero (fresh DB) in one command
2) upgraded safely via migrations
3) optionally seeded with known test users/data for local/dev

## Scope
- Alembic sanity wiring (baseline + upgrade path)
- Bootstrap/seed command that is safe, deterministic, idempotent where possible
- Tests that verify:
  - migrations run on an empty DB
  - schema is usable by critical tables
  - seed creates expected baseline entities

## Invariants (NON-NEGOTIABLE)
1) No breaking changes to existing runtime code paths.
2) No removal/renaming of existing models/fields/functions.
3) Migrations must preserve immutable records (snapshots, audits, jobs).
4) Bootstrap must never mutate completed snapshots post-creation.
5) If seed is re-run, it must not duplicate critical identity rows (users by email).

## Deliverables
- CLI:
  - `python -m app.cli.db upgrade`
  - `python -m app.cli.db seed`
  - `python -m app.cli.db fresh` (drop+create in dev only; optional)
- Alembic directory present and configured
- Minimal seed dataset:
  - admin/editor/viewer users (by email)
  - at least 1 project + 1 draft snapshot (optional, dev-only)

## Exit Criteria
- `upgrade` works on empty DB
- `seed` creates baseline users (idempotent)
- tests pass deterministically

