# Phase R — AI Engineering Assistant

## Purpose
Provide engineering reasoning, analysis, and proposals without mutating system state.

---

## Assistant Capabilities

The assistant MAY:
- Analyze geometry
- Explain validation failures
- Perform calculations
- Propose modifications
- Compare alternatives

The assistant MUST NOT:
- Modify geometry
- Modify snapshots
- Execute commands
- Bypass permissions
- Persist data

---

## Interaction Modes

- inquiry      → explanation only
- calculation  → numeric reasoning
- proposal     → suggested changes
- review       → pass / fail / conditional

---

## Context Envelope

```json
{
  "snapshot_id": "uuid",
  "project_id": "uuid",
  "user_role": "viewer|editor|owner|admin",
  "selected_entities": ["panel-1", "curve-3"],
  "active_constraints": [],
  "validation_errors": []
}

