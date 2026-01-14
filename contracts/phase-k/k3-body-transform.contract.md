# Phase K.3 — Body Transformations (Safe Subset)

Status: DRAFT
Phase: K.3
Scope: Controlled body geometry transformations
Depends on: Phase I, Phase K.0–K.2, Phase S

---

## 1. Purpose

Phase K.3 introduces **body geometry mutations** that:

- Affect vehicle shape
- Do NOT alter topology
- Are fully deterministic
- Are snapshot-based and journaled

This phase exists to make `body_state` a first-class mutation domain.

---

## 2. Core Rules (NON-NEGOTIABLE)

1. No in-place snapshot mutation
2. No topology-breaking operations
3. No freeform geometry edits
4. Every mutation is preset-based
5. Every mutation creates a new snapshot
6. Every mutation writes a journal entry

Violation of any rule invalidates Phase K.3.

---

## 3. Capability Gate

Required workspace capability:

```json
{
  "canModifyBody": true
}

