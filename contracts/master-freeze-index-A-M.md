# Graffi-Tech-Mat — Master Freeze Index (Phases A–M)

This document records all **frozen architectural phases** from A through M.
Frozen phases are **immutable**: behavior may be extended only through later phases.

Breaking a frozen phase is considered an architectural regression.

---

## 🧱 FOUNDATIONAL PHASES (A–G)

### Phase A — Vision & Hard Limits ✅ FROZEN
- Parametric, intent-first system
- No destructive edits
- Level-2 geometry, Level-3 upgradeable
- Engineering is additive, never mutative

---

### Phase B — Domain Model (Language Freeze) ✅ FROZEN
Core entities:
- Vehicle
- ReferencePlane
- Curve
- Surface
- Panel
- Parameter
- Constraint
- Snapshot
- ExportArtifact

❌ No manufacturing semantics here

---

### Phase C — Data Authority ✅ FROZEN
- Single source of truth
- Derived data regenerable
- No stored meshes as authority

---

### Phase D — Identity & Trust ✅ FROZEN
- Every mutation has an actor
- Audit trail mandatory

---

### Phase E — Access Control ✅ FROZEN
- Viewer / Editor / Owner / Admin
- Capabilities > UI flags

---

### Phase F — Persistence & Consistency ✅ FROZEN
- Deterministic serialization
- Rollback-safe snapshots
- Migration-ready state

---

### Phase G — Modularization ✅ FROZEN
- Engine isolated
- Geometry isolated
- Automation isolated
- No cross-layer coupling

---

## ⚙️ CORE PLATFORM PHASES (H–M)

---

### Phase H — Core Runtime ✅ FROZEN
- Scene runtime
- Plugin boundaries
- No editor state leaks

---

### Phase I — Invariants & Safety ✅ FROZEN
- Symmetry enforcement
- Reference integrity
- Forbidden states blocked at source

---

### Phase J — Creation Primitives (Intent Birth)

#### J.1 — Parametric Curves ✅ FROZEN
- Numeric control points
- Constraint-ready
- Deterministic evaluation

#### J.2 — Curve Constraints ✅ FROZEN
- Tangency
- Coincidence
- Symmetry
- Dimensional constraints

#### J.3 — Constraint Evaluation & Solving ✅ FROZEN
- Deterministic solver
- No silent failures
- Human-readable errors

#### J.5 — Workspace Normalization (Optional) ✅ FROZEN
- Snapshot filtering by status
- Ordering guarantees
- Stable editor state

---

### Phase K — Body Construction (Level-2 Geometry)

#### K.1 — Curve → Surface Generation ✅ FROZEN
- Loft / sweep
- No thickness
- No materials

#### K.2 — Panel Segmentation ✅ FROZEN
- Logical panels (doors, roof, sides)
- Panels reference surfaces
- No geometry duplication

#### K.3 — Panel Parameters ✅ FROZEN
- Length, rake, offsets
- Numeric only
- Parameters never mutate geometry

---

### Phase L — Geometry Validation (Level-2) ✅ FROZEN
Validation includes:
- Minimum curvature
- Self-intersection
- Panel overlap
- Continuity
- Symmetry violations

Failures:
- Block exports
- Do NOT delete geometry

---

### Phase M — Immutable Outputs ✅ FROZEN
- Deterministic exports
- Snapshot-bound
- No mutation post-export
- Meshes are derived, never authoritative

---

## 🔒 GLOBAL INVARIANTS (A–M)

1. Snapshots are immutable once completed
2. Draft edits always create new snapshots
3. Geometry intent precedes representation
4. Validation blocks output, not design
5. Audit is the system of record
6. UI never decides authority
7. Automation never bypasses rules

---

## ⛔ OUT OF SCOPE (NOT YET ACTIVE)

- Manufacturing semantics (Level 3)
- Thickness, welds, tolerances
- Physics simulation
- Video / animation
- AI-driven geometry edits

These belong to later phases (K-E, L-E, M-E, R).

---

## 🧊 FREEZE DECLARATION

Phases A through M are **frozen**.

All future work MUST:
- Extend via new phases
- Respect snapshot immutability
- Preserve audit integrity

Breaking a frozen phase requires:
- Explicit migration phase
- Versioned contracts
- Full audit trail

---

**Signed-off:**  
Graffi-Tech-Mat Architecture  
**Freeze Level:** AAA / Enterprise-grade  

