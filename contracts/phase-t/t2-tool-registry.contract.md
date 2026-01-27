# Phase T.2 — Tool Registry

## Purpose
Define the authoritative registry of all legal tools and their execution rules.

---

## Tool Definition

A Tool is a declarative description of an action.

Each tool declares:
- required station
- allowed snapshot state
- required capability
- operation identifier

---

## Core Rules

- Tools must be registered before use
- Tool execution is blocked if:
  - station mismatch
  - snapshot state mismatch
  - capability missing
- Tools do not bypass constraints
- Tools do not mutate completed snapshots

---

## Snapshot Rules

| Snapshot Status | Tool Execution |
|---------------|----------------|
| draft         | allowed (if tool permits) |
| completed     | forbidden |
| failed        | forbidden |

---

## Forbidden

- Ad-hoc tool execution
- UI-only validation
- Tools without registry entry

