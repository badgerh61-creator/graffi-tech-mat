# Phase T.4 — Mode Enforcement

## Purpose
Define authoritative execution modes and enforce them for all tools.

---

## Modes

- editing
- review
- read_only

---

## Mode Rules

editing:
- Allowed: transform, constraint, validate
- Forbidden: finalize without validation

review:
- Allowed: validate, inspect
- Forbidden: transform, constraint, finalize

read_only:
- Allowed: inspect only
- Forbidden: all execution

---

## Mode Resolution

Mode is derived from:
- snapshot status
- station
- user capability
- explicit transitions

---

## Forbidden

- UI-only mode switches
- Executing tools outside mode
- Silent mode changes

