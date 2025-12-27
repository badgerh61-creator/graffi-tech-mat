# Phase F4.1 — Organization Foundations (FROZEN)

## Scope
- Organizations table
- Organization members table
- Basic organization membership roles
- No impact on models or assets

## Explicitly Excluded
- Organization-owned models
- Organization access to models
- Ownership transfer
- Organization-scoped creation

## Invariants
- Organizations are isolated containers
- Membership is explicit via organization_members
- No implicit permissions granted

## Verification
- Organizations can be created
- Users can be added as members
- Unique constraints enforced
- No regression in user-owned models

## Freeze Date
- 2025-01-XX

