# Phase K.2 — Engine Tune Preset Contract

**Phase:** K.2  
**Domain:** Tuning (Engine)  
**Status:** Draft  
**Mutation Type:** Preset-based, deterministic

---

## Purpose

Introduce controlled, preset-based engine tuning mutations that:

- Are deterministic
- Are snapshot-based
- Are fully journaled
- Do not invoke simulation or physics
- Do not directly mutate engine state

This mutation exists to **express intent**, not simulate behavior.

---

## Allowed Presets

Engine tuning is restricted to **explicit presets**.

```json
["eco", "stock", "sport", "race"]

