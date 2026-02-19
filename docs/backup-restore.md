# Backup / Restore

## Backup (Postgres)
pg_dump "$DATABASE_URL" > backup.sql

## Restore (Postgres)
psql "$DATABASE_URL" < backup.sql

## Invariants
- Restores must preserve audit integrity and immutable snapshots.
- Never manually edit audit rows.

