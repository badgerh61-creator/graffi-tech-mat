# Phase E.2 — Tool Availability & Flow Guidance

## Purpose
Expose kernel-evaluated tool availability and legal flow guidance to the UI.

---

## Tool Availability

Each tool MUST expose:

- tool_id
- availability: allowed | blocked
- reason (optional)
  - code
  - message

Availability MUST be derived from:
- Station (Phase T.1)
- Mode (Phase T.4)
- Snapshot state
- Draft ownership (Phase U)
- Constraints

---

## Flow Guidance

Kernel MAY expose:

- next_allowed_tools: [tool_id]
- blocked_flows: [
    {
      attempted_tool,
      reason
    }
  ]

---

## Guarantees

- UI must not compute availability
- UI must not reorder flows
- UI must not hide kernel reasons
- Reasons must be human-readable

---

## Forbidden

- UI-derived availability
- Silent disabling
- Guessing next steps
- Auto-selection of tools

