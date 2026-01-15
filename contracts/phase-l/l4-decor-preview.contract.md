# Phase L.4 — Decor Preview Rendering (Read-Only Proof Mode)

**Phase:** L  
**Stage:** L.4  
**Status:** DRAFT (freeze after verification)  
**Scope:** Read-only decor preview rendering  
**Depends on:**  
- Phase J — Workspace & snapshot resolution  
- Phase K.1 — Decor mutations (apply-decal, remove-decal, set-material, swap-bodykit)

---

## 1. Purpose

Phase L.4 defines the **read-only preview contract** for rendering decor changes
produced by Phase K mutations.

This phase exists to **prove** that decor mutations:

- are renderable
- are deterministic
- do not require engine-side mutation
- can be safely previewed without persistence

Phase L.4 introduces **no write paths**.

---

## 2. Non-Negotiable Guarantees

The following guarantees MUST hold at all times:

1. No database writes
2. No snapshot mutations
3. No journal entries
4. No engine-side persistence
5. No editor state mutation

If any guarantee is violated, Phase L.4 is invalid.

---

## 3. Inputs

Phase L.4 operates exclusively on **existing snapshots**.

### Required Input

```json
{
  "project_id": "uuid",
  "snapshot_id": "uuid"
}

