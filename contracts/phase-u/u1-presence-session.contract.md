# Phase U.1 — Presence & Session Authority

## Purpose
Define how users declare presence and gain execution authority in the Studio Kernel.

---

## Presence

- Presence is explicit
- Presence does not grant mutation rights
- Presence is scoped to a project

---

## Sessions

- A session represents execution authority
- Sessions are scoped to:
  - user_id
  - project_id
  - optional snapshot_id
- Sessions have a TTL
- Expired sessions are invalid

---

## Authority Rules

- No tool execution without an active session
- Session must match project context
- Snapshot-scoped actions require snapshot-scoped session

---

## API

POST /projects/{project_id}/presence/join  
POST /projects/{project_id}/presence/leave  

POST /projects/{project_id}/sessions/start  
POST /projects/{project_id}/sessions/end  

---

## Audit Events

- presence.joined
- presence.left
- session.started
- session.expired
- session.denied

---

## Forbidden

- Implicit presence
- Tool execution without session
- Cross-project session reuse
- UI-implied authority

