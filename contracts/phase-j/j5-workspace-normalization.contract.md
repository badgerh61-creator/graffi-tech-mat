# Phase J.5 — Workspace Normalization

## Purpose
Finalize workspace semantics to ensure deterministic behavior and safe querying.

---

## Snapshot Visibility Rules

Snapshots have an explicit status:

- `completed`
- `failed`
- `pending` (optional, transient)

### Default Visibility

- Workspace APIs MUST return only `completed` snapshots by default
- `failed` snapshots are hidden unless explicitly requested
- `pending` snapshots are never returned to the UI

---

## Snapshot Query Contract

```json
{
  "workspace_id": "uuid",
  "snapshots": [
    {
      "id": "uuid",
      "status": "completed",
      "created_at": "iso-8601"
    }
  ]
}

