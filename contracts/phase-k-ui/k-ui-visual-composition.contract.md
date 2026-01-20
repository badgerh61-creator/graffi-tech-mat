# Phase K-UI — Visual Composition UI Binding

## Status
AUTHORITATIVE CONTRACT

---

## Purpose

Bind Level-2 geometry operations to editor UI controls in a safe,
deterministic, and reversible manner.

Phase K-UI defines **how humans interact with Level-2 geometry**.
It does not define geometry itself.

---

## Scope

### Does

- Bind parametric controls to geometry regeneration
- Dispatch explicit numeric commands to the engine
- Enforce symmetry at the UI boundary
- Support deterministic undo / redo
- Surface geometry validation results (read-only)

### Does NOT

- Modify geometry directly
- Author or mutate surfaces or panels
- Auto-fix validation errors
- Introduce materials, thickness, or fabrication logic
- Store derived meshes

---

## UI → Engine Interaction Model

- UI emits **commands only**
- Commands are:
  - Explicit
  - Numeric
  - Serializable
- Engine is the sole authority that mutates geometry
- UI state must never diverge from engine state

---

## Supported Commands (Level-2 Only)

### SET_PARAM

Adjust a parametric dimension.

```json
{
  "command": "SET_PARAM",
  "param": "length | height | width | rake | roof_arc",
  "value": "number"
}

