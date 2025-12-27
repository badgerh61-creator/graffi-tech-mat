# Phase F4.3 — Organization Model Access (FROZEN)

## Scope
- Organization members can access organization-owned models
- Access integrated into existing CRUD queries
- Owner checks extended to organization context

## Explicitly Excluded
- Organization-scoped model creation
- Ownership transfer (user ⇄ org)
- Organization admin role escalation
- UI changes

## Invariants
- User-owned models unchanged
- Collaboration permissions unchanged
- Admin override preserved
- No schema or migration changes

## Verification
- Org members can list org-owned models
- Non-members cannot access org-owned models
- User-owned and shared models still work
- Exports and assets unaffected

## Freeze Date
- 2025-01-XX

