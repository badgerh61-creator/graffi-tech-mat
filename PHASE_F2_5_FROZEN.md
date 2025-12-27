# PHASE F2.5 — FROZEN

## Scope
Organization-aware model access checks.

This phase finalizes how model access is resolved when a model is owned
by either a user or an organization.

## Included
- Canonical model ownership resolution via `ModelOwner`
- Organization membership lookup via `OrganizationMember`
- User-owned model fallback preserved
- Access enforcement distinguishes:
  - user-owned models
  - organization-owned models
- Admin override remains unchanged

## Excluded
- Organization-owned model creation
- Ownership transfer (user ⇄ organization)
- Organization-scoped model invites
- Any database schema changes
- Any new API routes

## Compatibility
- Backward compatible with all prior phases
- Existing user-owned models behave exactly as before
- Collaboration permissions remain unchanged

## Notes
- No Alembic migrations introduced
- Access logic only (no writes)
- Serves as prerequisite for Phase F2.6

## Status
Frozen and stable.

