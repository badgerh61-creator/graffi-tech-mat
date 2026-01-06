# Phase I.3 — Set Active Snapshot (API Contract)

## Purpose
Change which snapshot is authoritative for editor boot, without mutating scene data.

This mutation only switches a pointer.
It does not recompute, invalidate, or regenerate any state.

---

## Endpoint

POST /projects/{project_id}/mutations/set-active-snapshot

---

## Authorization

Required capability:

- canSetActiveSnapshot

Allowed roles:
- Editor
- Owner
- Admin

Viewers are explicitly forbidden.

---

## Request

### Path Parameters
- project_id: UUID

### Body
```json
{
  "snapshot_id": "uuid"
}

