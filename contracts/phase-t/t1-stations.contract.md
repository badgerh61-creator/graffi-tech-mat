# Phase T.1 — Studio Stations

## Purpose
Define authoritative operating contexts ("stations") for all studio actions.

A station represents *where* a user is operating semantically,
not visually.

---

## Station Definition

A station:
- Is mutually exclusive
- Gates which tools may execute
- Is required for every action
- Is explicitly transitioned
- Is auditable

---

## Canonical Stations

- geometry
- curve
- panel
- validation
- review

---

## Rules

- A user must always be in exactly one station
- Tools may only execute if allowed by the active station
- Station transitions must be explicit
- Station authority is server-side
- UI may only request station changes

---

## Forbidden

- Implicit station switching
- Tool execution without station context
- UI-derived station authority

