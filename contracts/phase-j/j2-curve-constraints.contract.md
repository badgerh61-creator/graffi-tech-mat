# Phase J.2 — Curve Constraints

## Purpose
Define declarative geometric constraints attached to parametric curves.

---

## Constraint Definition

A constraint consists of:
- constraint_id
- type
- target_curve_id
- reference (optional)
- parameters (numeric only)

---

## Allowed Constraint Types (Initial)

- horizontal
- vertical
- parallel
- perpendicular
- coincident
- symmetric
- fixed_length

---

## Constraint Rules

- Constraints attach to curves
- Constraints are declarative
- Constraints do not mutate geometry in J.2
- Constraints exist only in draft snapshots
- Adding a constraint creates a new draft snapshot
- Constraints are immutable in completed snapshots

---

## API Endpoint

POST /projects/{project_id}/snapshots/{snapshot_id}/curves/{curve_id}/constraints

---

## Request Shape

```json
{
  "type": "horizontal",
  "reference": "x-axis",
  "params": {}
}
```

---

## Success Response

```json
{
  "snapshot_id": "uuid",
  "constraint_id": "uuid"
}
```

---

## Failure Modes

| Condition | HTTP |
|---------|------|
| Snapshot not draft | 409 |
| Curve not found | 404 |
| Invalid constraint type | 422 |
| Permission denied | 403 |

---

## Forbidden

- Solving constraints
- Mutating curve geometry
- Implicit constraints
- Editing constraints in completed snapshots

