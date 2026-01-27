# Phase T.3 — Flow Graph (Legal Sequences)

## Purpose
Define the authoritative legal execution sequences for tools.

---

## Flow Definition

A Flow is a directed graph of allowed transitions
between tool operations.

---

## Canonical Flow

draft
  → transform
  → constraint
  → validate
  → finalize

---

## Rules

- Tool execution is allowed only if it follows a legal edge
- Flow state is inferred from snapshot lineage
- Failed tools do not advance flow
- Completed snapshots terminate the flow

---

## Forbidden

- Skipping validation before finalize
- Executing finalize twice
- Executing transforms after finalize
- UI-driven flow assumptions

