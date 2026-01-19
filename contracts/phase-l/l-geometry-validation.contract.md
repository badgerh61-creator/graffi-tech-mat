# Phase L — Geometry Validation (Level-2)

## Purpose
Ensure generated geometry is valid, symmetric, and export-safe.

---

## Validation Targets

- Surfaces
- Panels
- Panel adjacency
- Symmetry constraints

---

## Validation Rules

### Curvature
- Minimum curvature radius enforced
- Prevents pinching and surface collapse

### Intersection
- Panels may not self-intersect
- Adjacent panels may not overlap

### Symmetry
- Surfaces must respect reference-plane symmetry
- Asymmetry is forbidden at Level-2

### Continuity
- Adjacent panels must be position-continuous (C0)
- Tangency (C1) is recommended but not required

---

## Validation Output

```json
{
  "valid": false,
  "errors": [
    {
      "code": "MIN_CURVATURE_VIOLATION",
      "message": "Surface curvature below minimum threshold",
      "entity_id": "surface-uuid"
    }
  ]
}

