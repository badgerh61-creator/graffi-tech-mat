# Graffi-Tech-Mat — Phase 4.6 Complete

## Status
✅ STABLE  
✅ RBAC enforced  
✅ Status-free invites  
✅ SQLite-safe  
✅ No pending migrations  

## Confirmed Behaviors

### Authentication
- JWT access tokens issued via `/login`
- Invalid tokens → 401
- Valid tokens → role-checked access

### Roles
- Viewer: read-only
- Editor: create models, invite users
- Admin: full access

### Models
- Viewer cannot create models (403)
- Editor/Admin can create models (200)
- Users only see models they:
  - Own
  - Are invited to
  - Belong to via organization

### Invites
- Existing user → auto-accept
- New user → invite record created
- Invite acceptance deletes invite
- No `status` column
- No migrations required

### Assets
- GLB URL only returned if:
  - User has access
  - Asset is `.glb`
  - Asset status is `ready`

### Non-Goals (Intentionally Missing)
- Activity feed
- Real-time collaboration
- Video simulation
- AI rendering

## Freeze Rules
- No schema changes
- No RBAC changes
- No new endpoints
- Only bugfixes allowed after this point

## Tag
`v1.0-backend-rbac-stable`

