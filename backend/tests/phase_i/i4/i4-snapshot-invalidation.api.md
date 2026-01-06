# Phase I.4 — Snapshot Invalidation (API Contract)

## Purpose
Mark a completed snapshot as obsolete without deleting it,
while preserving auditability and editor boot determinism.

---

## Endpoint

POST /snapshots/{snapshot_id}/mutations/invalidate

---

## Authorization

Required capability:
- canInvalidateSnapshot

Allowed roles:
- Editor
- Owner
- Admin

Viewers are forbidden.

---

## Preconditions (ALL REQUIRED)

1. Snapshot exists
2. Snapshot.status === "completed"
3. Snapshot is not already obsolete
4. Parent project is not archived

---

## Failure Modes

| Condition | HTTP | Reason |
|--------|------|--------|
| Snapshot pending | 409 | Snapshot not finalized |
| Snapshot failed | 409 | Failed snapshots are terminal |
| Snapshot obsolete | 409 | Already invalidated |
| Project archived | 403 | Project is read-only |

---

## Success Response

```json
{
  "snapshot_id": "uuid",
  "status": "obsolete"
}

