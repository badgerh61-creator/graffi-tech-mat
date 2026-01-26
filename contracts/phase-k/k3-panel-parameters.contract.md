# Phase K.3 — Panel Parameters

## Purpose
Attach parametric dimensions to panels without modifying geometry.

---

## Supported Parameters (Level 2)

- length_offset (float, mm)
- rake_angle (float, degrees)
- lateral_offset (float, mm)
- vertical_offset (float, mm)

---

## Snapshot Lifecycle

- draft → draft (success)
- draft → failed (invalid params)
- completed → forbidden

---

## API Endpoint

POST /projects/{project_id}/snapshots/{snapshot_id}/panels/parameters

---

## Request Body

```json
{
  "panel_id": "panel-1",
  "parameters": {
    "length_offset": 120,
    "rake_angle": 5.5
  }
}
```

---

## Preconditions

- Snapshot exists
- Snapshot.status == "draft"
- Panel exists on snapshot
- User has editor permissions

---

## Success Response

```json
{
  "snapshot_id": "uuid",
  "status": "draft",
  "updated_panel_id": "panel-1"
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
      "reason": "invalid_parameter"
    }
  ]
}
```

---

## Audit

Parameter application MUST emit:

- action: panel.parameters.applied
- snapshot_id (new)
- parent_snapshot_id
- panel_id
- parameters_changed
- timestamp

---

## Forbidden

- Geometry mutation
- Non-numeric parameters
- Editing completed snapshots
- Implicit parameter defaults

