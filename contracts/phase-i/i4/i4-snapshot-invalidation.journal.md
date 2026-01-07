
---

## 📄 FILE 2  
### `contracts/phase-i/i4/i4-snapshot-invalidation.journal.md`

```md
# Phase I.4 — Snapshot Invalidation (Journal Contract)

## Purpose
Provide an immutable audit trail for snapshot invalidation events.

---

## Journal Entry Type

INVALIDATE_SNAPSHOT

---

## Schema

```json
{
  "type": "INVALIDATE_SNAPSHOT",
  "snapshot_id": "uuid",
  "project_id": "uuid",
  "actor_user_id": "uuid",
  "timestamp": "iso-8601"
}

