# Phase J — Workspace Contract (Frozen)

Status: FROZEN  
Phase: J  
Scope: Editor Boot & Read-Only State Assembly

---

## Purpose

This document defines the canonical workspace payload used to boot the editor.
It guarantees deterministic, capability-aware, read-only initialization.

This contract is frozen at the end of Phase J.

---

## Authoritative Endpoint

GET /workspace/{project_id}

This endpoint is the sole source of truth for editor boot.

---

## Required Top-Level Fields

The workspace payload MUST include:

- project
- snapshots
- assets
- jobs
- capabilities

These fields MUST NOT be removed or renamed.

---

## Semantic Guarantees

- Workspace is read-only
- Mutations occur only through Phase I mutation endpoints
- Snapshots are immutable
- active_snapshot_id determines editor state
- Capabilities are server-derived and authoritative

---

## Extension Policy

Future phases may:

- Add new fields
- Extend nested structures
- Introduce new capability flags

Future phases may NOT:

- Break editor boot determinism
- Mutate state via workspace
- Change meanings of existing fields

---

## Notes

This contract protects Phase K and beyond.
It does not restrict feature growth.

