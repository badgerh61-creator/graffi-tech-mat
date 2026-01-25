# Phase J.3 — Constraint Evaluation & Solving

## Purpose
Evaluate and solve declarative curve constraints to produce updated geometry.

---

## Solver Lifecycle

1. Input snapshot (draft only)
2. Extract curves + constraints
3. Evaluate constraint consistency
4. Solve numeric parameters
5. Produce new draft snapshot

---

## Snapshot Outcomes

- draft → draft (success)
- draft → failed (unsatisfiable)
- completed → forbidden

---

## API Endpoint

POST /projects/{project_id}/snapshots/{snapshot_id}/solve

---

## Preconditions

- Snapshot exists
- Snapshot.status == "draft"
- User has editor permissions

---

## Success Response

```json
{
  "snapshot_id": "uuid",
  "status": "draft",
  "solved": true
}
```

---

## Failure Response (Constraint Conflict)

```json
{
  "snapshot_id": "uuid",
  "status": "failed",
  "errors": [
    {
      "constraint_id": "uuid",
      "reason": "unsatisfiable"
    }
  ]
}
```

---

## Failure Modes

| Condition | HTTP |
|--------|------|
| Snapshot not draft | 409 |
| Permission denied | 403 |
| Solver crash | 500 |

---

## Audit

Solver execution MUST emit:

- action: curve.constraints.solved
- snapshot_id (new)
- parent_snapshot_id
- success / failure
- error summary (if failed)

---

## Forbidden

- Partial solves
- Geometry mutation in-place
- Auto-removal of constraints
- Silent failure

