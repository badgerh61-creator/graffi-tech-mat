# Phase K.2 — Panel Segmentation

## Purpose
Segment generated surfaces into logical body panels (doors, roof, sides).

---

## Panel Types (Level 2)

- door
- roof
- side
- hood
- trunk
- custom

---

## Snapshot Lifecycle

- draft → draft (success)
- draft → failed (invalid segmentation)
- completed → forbidden

---

## API Endpoint

POST /projects/{project_id}/snapshots/{snapshot_id}/panels/segment

---

## Preconditions

- Snapshot exists
- Snapshot.status == "draft"
- Snapshot contains generated surfaces
- User has editor permissions

---

## Request Body

```json
{
  "panels": [
    {
      "type": "door",
      "surface_ids": ["surface-1"],
      "label": "front-left-door"
    }
  ]
}
```

---

## Success Response

```json
{
  "snapshot_id": "uuid",
  "status": "draft",
  "panels_created": 1
}
```

---

## Failure Response

```json
{
  "snapshot_id": "uuid",
  "status": "failed",
  "errors": [
    {
      "reason": "surface_not_found"
    }
  ]
}
```

---

## Audit

Panel segmentation MUST emit:

- action: panel.segmented
- snapshot_id (new)
- parent_snapshot_id
- panel_count
- timestamp

---

## Forbidden

- Surface mutation
- Overlapping panel regions
- Implicit panel inference
- Panel geometry generation

