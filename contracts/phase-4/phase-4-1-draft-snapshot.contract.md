# Phase 4.1 — Draft Snapshot Creation

## Endpoint

POST /snapshots/{snapshot_id}/draft

---

## Purpose

Create a mutable draft snapshot from a completed snapshot.

---

## Preconditions

- User authenticated
- User has editor or admin role
- Snapshot exists
- Snapshot status == "completed"
- Project has no existing draft snapshot

---

## Behavior

- Clone scene_state_hash
- status = "draft"
- is_editable = true
- created_at = now
- Parent snapshot remains unchanged

---

## Success Response

```json
{
  "id": 42,
  "status": "draft",
  "parent_snapshot_id": 12
}

