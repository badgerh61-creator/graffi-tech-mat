# Phase K — Visual Composition (Level-2 Geometry)

## Purpose
Transform parametric intent (curves + references) into visible vehicle geometry.

---

## Core Concepts

### Surface
A mathematically derived shape generated from one or more curves.

### Panel
A bounded surface region representing a logical body section.

---

## Allowed Operations

- Loft (curve → surface)
- Sweep (profile along path)
- Symmetry mirror (reference plane)
- Panel segmentation (non-destructive)

---

## Surface Generation Rules

- Surfaces are derived, not authored
- Regeneration must be deterministic
- Surfaces reference source curves
- No direct vertex manipulation allowed

---

## Panel Rules

- Panels reference surfaces
- Panels do not alter surface geometry
- Panels define logical regions only
- Panels are addressable by ID

---

## Parametric Controls

Sliders may control:
- Length
- Height
- Width
- Rake
- Roof arc

Sliders:
- Must be numeric
- Must regenerate geometry
- Must not store meshes

---

## Symmetry Rules

- Symmetry enforced via reference planes
- Asymmetric edits are forbidden at Level-2
- Breaking symmetry requires Level-3 override (future)

---

## Determinism Guarantee

Given:
- Same curves
- Same parameters
- Same reference planes

The system MUST regenerate identical geometry.

---

## Forbidden

- Thickness
- Materials
- UV mapping
- Boolean destructive edits
- Freeform sculpting

