# PHASE F3 — Collaboration UX & Operational Readiness (FROZEN PLAN)

## Status
🟡 Planned  
⏳ Not yet implemented  
🔒 Must not modify backend ownership, permissions, or schemas

---

## Purpose

Phase F3 exists to **stabilize and clarify collaboration UX** built on top of
the already frozen ownership and permission system (Phases F1–F2.6).

This phase improves **visibility, predictability, and safety** without adding
new business logic or expanding scope into product features.

---

## Explicit Constraints (Non-Negotiable)

- ❌ No database migrations
- ❌ No ownership logic changes
- ❌ No permission rules changes
- ❌ No new backend APIs
- ❌ No org-wide features
- ❌ No realtime features

Frontend-only refinements and UX hardening are allowed.

---

## Scope Breakdown

### F3.1 — Permission Visibility (UI Only)

**Goal:** Users always understand *why* actions are enabled or disabled.

Deliverables:
- Visible role indicator (viewer / editor / owner)
- Explicit read-only mode banner
- Disabled controls include tooltips explaining why
- Upload and edit actions visually locked for viewers

---

### F3.2 — Invite Lifecycle UX

**Goal:** Make invite behavior predictable and transparent.

Deliverables:
- Invite expiration countdown (client-side only)
- Visual expired state for invites
- Resend invite action (reuses existing endpoint)
- Dismissable invite banner in Studio
- Clear messaging for expired or revoked invites

---

### F3.3 — Per-Model Collaboration Panel Hardening

**Goal:** Make collaboration management safe and self-explanatory.

Deliverables:
- Share modal empty states clarified
- Owner-only actions clearly labeled
- Confirmation dialogs standardized
- Loading and error states consistent
- No new collaboration concepts introduced

---

### F3.4 — Activity Feed Fallback (Frontend Safety)

**Goal:** Prevent UX breakage if backend activity endpoint is absent.

Deliverables:
- Graceful fallback if `/activity` returns 404
- Placeholder message (“Activity coming soon”)
- Suppress repeated error spam
- No backend implementation required

---

### F3.5 — Session & Refresh Hardening

**Goal:** Eliminate auth-related UX edge cases.

Deliverables:
- Single refresh attempt per boot
- Silent logout on refresh failure
- Prevent infinite refresh loops
- Clear user feedback on session expiry

---

## Explicitly Out of Scope

The following are intentionally deferred to later phases:

- Org-wide invite management
- Email delivery infrastructure
- Realtime presence / cursors
- Activity backend implementation
- Monetization
- Audit dashboards

---

## Exit Criteria (Freeze Conditions)

Phase F3 is considered complete when:

- Permission state is always visible and understandable
- Invite UX is predictable and reversible
- No collaboration confusion remains
- No backend logic was modified
- No schema changes occurred

Once frozen, **Phase F (Collaboration & Ownership) is fully complete**.

---

## Next Phase

➡️ Phase G — Product Features (Decals, Materials, Export, Scenes)

Phase F3 must be frozen before Phase G begins.

