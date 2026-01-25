# Phase K.1 — Curve → Surface Generation

## Purpose
Generate parametric surfaces from solved curves.

---

## Supported Surface Types (Level 2)

- loft
- sweep
- patch (boundary surface)

---

## Snapshot Lifecycle

- draft → draft (success)
- draft → failed (invalid curves)
- completed → forbidden

---

## API Endpoint

POST /projects/{project_id}/snapshots/{snapshot_id}/surfaces/generate

---

## Preconditions

- Snapshot exists
- Snapshot.status == "draft"
- Curves are solved
- User has editor permissions

---

## Success Response

```json
{
  "snapshot_id": "uuid",
  "status": "draft",
  "surfaces_created": 3
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
      "reason": "curve_topology_invalid"
    }
  ]
}
```

---

## Audit

Surface generation MUST emit:

- action: surface.generated
- snapshot_id (new)
- parent_snapshot_id
- surface_count
- timestamp

---

## Forbidden

- Mesh triangulation
- Geometry mutation in-place
- Implicit surface repair
- Auto-thickening

