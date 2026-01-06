
---

## 📄 FILE 2  
### `contracts/phase-i/i3/i3-set-active-snapshot.journal.md`

```md
# Phase I.3 — Set Active Snapshot (Journal Contract)

## Purpose
Provide a complete, append-only, reversible audit trail
for active snapshot switching.

The journal is the source of truth for undo and historical reconstruction.

---

## Journal Entry Type

SET_ACTIVE_SNAPSHOT

---

## Schema

```json
{
  "type": "SET_ACTIVE_SNAPSHOT",
  "project_id": "uuid",
  "from_snapshot_id": "uuid | null",
  "to_snapshot_id": "uuid",
  "actor_user_id": "uuid",
  "timestamp": "iso-8601"
}

