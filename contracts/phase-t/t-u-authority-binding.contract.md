# Phase T-U — Studio Kernel Authority Binding

## Purpose
Bind collaboration authority (U.2–U.4) into tool execution and flow enforcement.

---

## Tool Execution Rules

Before executing any tool:

1. Active session must exist (U.1)
2. Tool must be valid in current station (T.1)
3. Tool must be allowed in current mode (T.4)
4. Snapshot must be draft for mutating tools
5. Caller must own the draft (U.2)
6. Draft must be conflict-free (U.3)

---

## Flow Rules

- Flow transitions are blocked if:
  - Ownership is lost
  - Conflict is detected
  - Session expires

---

## Ownership Transfer

- Authority transfer only via:
  POST /snapshots/{id}/handoff

- Tools may not implicitly reassign ownership

---

## Failure Semantics

| Violation | HTTP |
|---------|------|
| No session | 403 |
| Not owner | 403 |
| Conflict | 409 |
| Wrong station | 409 |
| Wrong mode | 409 |

---

## Audit Events

- tool.execution.denied
- flow.transition.denied
- authority.violation

---

## Forbidden

- UI-based authority
- Silent ownership change
- Tool-level permission checks outside kernel

