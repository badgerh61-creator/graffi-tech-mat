# Level-2 Freeze — Visual Geometry & Immutable Outputs (K–M)

## Status
FROZEN

## Scope
This freeze applies to:
- Phase K — Visual Composition (Level-2 Geometry)
- Phase L — Geometry Validation (Level-2)
- Phase M — Immutable Outputs (Exports)

---

## 1. Purpose

Level-2 defines the **complete visual and geometric representation of a vehicle**,
suitable for visualization, validation, and real-world fabrication reference —
without embedding manufacturing semantics.

This freeze establishes Level-2 as:
- Stable
- Deterministic
- Non-destructive
- Upgrade-safe

---

## 2. Level-2 Definition (What Exists)

At Level-2, the system supports:

### Geometry
- Parametric curves (from Phase J)
- Derived surfaces (loft, sweep)
- Reference-plane symmetry
- Panel segmentation

### Validation
- Curvature constraints
- Self-intersection detection
- Panel overlap detection
- Continuity checks (C0)
- Symmetry enforcement

### Outputs
- Immutable export artifacts
- Deterministic hashing
- Snapshot-bound exports
- Multiple formats (raster, vector, 3D)

---

## 3. Core Guarantees (NON-NEGOTIABLE)

Level-2 guarantees the following:

1. Geometry is **derived, not sculpted**
2. Geometry regeneration is **deterministic**
3. Panels are **logical regions**, not geometry mutations
4. Validation never mutates geometry
5. Failed validation blocks exports
6. Exports are **immutable and write-once**
7. Exports never embed editor state
8. Same input → same output bytes

---

## 4. Explicit Non-Goals (LOCKED OUT)

Level-2 explicitly does NOT include:

- Material assignment
- Thickness
- Tolerances
- Welds or fasteners
- Manufacturing constraints
- Physics or simulation
- Freeform sculpting
- Boolean destructive edits
- AI-driven geometry changes

Any of the above belongs to **Level-3 or later**.

---

## 5. Authority Boundaries

### Geometry Authority
- Curves and parameters define shape
- Surfaces reference curves
- Panels reference surfaces
- No entity overrides a lower layer

### Validation Authority
- Validation reports errors only
- Validation never fixes geometry
- Errors are human-readable and deterministic

### Export Authority
- Exports reference snapshots
- Snapshots are immutable
- Exports never modify snapshots

---

## 6. Determinism Contract

Given:
- Same snapshot
- Same parameters
- Same export format

The system MUST produce:
- Identical geometry
- Identical export bytes
- Identical hashes

Breaking determinism **breaks this freeze**.

---

## 7. Change Control Policy

Any of the following actions BREAK the Level-2 freeze:

- Adding thickness or materials to panels
- Allowing asymmetric geometry at Level-2
- Allowing geometry mutation during export
- Adding manufacturing semantics to geometry
- Introducing auto-fix or AI geometry edits
- Making exports mutable or re-writable

Breaking the freeze requires:
1. A new phase designation (e.g. K-E, L-E, M-E)
2. New contracts
3. Explicit migration rules

---

## 8. Relationship to Level-3

Level-3 Engineering & Manufacturing:

- Attaches metadata to Level-2 entities
- Does NOT redefine curves or surfaces
- Does NOT change Level-2 validation rules
- Produces parallel exports (STEP, CNC, etc.)

Level-2 geometry remains the **source of truth**.

---

## 9. Compliance & Safety Posture

With this freeze, Level-2 geometry is:

- Auditable
- Reproducible
- Export-safe
- Fabrication-reference-safe
- Legally defensible as design intent

This enables later compliance without retrofits.

---

## 10. Final Declaration

Level-2 (Phases K–M) is hereby declared:

- Complete
- Frozen
- Deterministic
- Upgrade-safe
- Protected from manufacturing creep

All future work MUST treat Level-2 as **read-only** unless explicitly superseded
by a Level-3 phase.


