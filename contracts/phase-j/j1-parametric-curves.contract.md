# Phase J.1 — Parametric Curves

## Purpose
Define parametric, constraint-aware curves as the foundation of geometry.

---

## Curve Definition

A curve is defined by:
- curve_id
- type (line | arc | bezier)
- parameters (numbers only)
- reference_plane_id
- constraints []

---

## Allowed Curve Types (Initial)

- line
- arc
- cubic_bezier

---

## Curve Rules

- Curves are numeric, not sculpted
- Curves exist only in draft snapshots
- Curve creation creates a new draft snapshot
- Curves are immutable in completed snapshots
- Curves must reference a plane

---

## API Endpoints

POST /projects/{project_id}/snapshots/{snapshot_id}/curves

---

## Request Shape

```json
{
  "type": "line",
  "reference_plane_id": "front",
  "params": {
    "x1": 0,
    "y1": 0,
    "x2": 1200,
    "y2": 300
  },
  "constraints": ["horizontal"]
}
```

---

## Success Response

```json
{
  "snapshot_id": "uuid",
  "curve_id": "uuid"
}
```

---

## Failure Modes

| Condition | HTTP |
|---------|------|
| Snapshot not draft | 409 |
| Invalid params | 422 |
| Missing reference plane | 400 |
| Permission denied | 403 |

---

## Forbidden

- Editing curves in completed snapshots
- Freehand drawing
- Mesh-based curves
- Implicit plane inference

