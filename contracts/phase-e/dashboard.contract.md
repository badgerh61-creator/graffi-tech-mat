# Dashboard — Projects & Activity

## Purpose
Provide a read-only overview of projects and recent system activity.

---

## Scope

The Dashboard shows:
- Projects the user can access
- Project metadata
- Recent activity events
- Snapshot and export summaries

The Dashboard does NOT allow:
- Creating projects
- Editing snapshots
- Triggering exports
- Changing modes or stations

---

## Entities

### ProjectSummary
- project_id
- name
- created_at
- owner_id
- snapshot_count
- last_activity_at

### ActivityItem
- action
- actor_user_id
- resource_type
- resource_id
- created_at
- summary (human-readable)

---

## API Endpoints (Read-Only)

GET /dashboard/projects
GET /dashboard/activity

---

## Permissions

- viewer → allowed
- editor → allowed
- owner → allowed
- admin → allowed

---

## Invariants

- Only accessible projects are returned
- Activity is ordered newest → oldest
- Activity reflects audit log truth
- No mutation side effects

---

## Forbidden

- Mutating endpoints
- Client-side aggregation guesses
- Hidden filtering logic

