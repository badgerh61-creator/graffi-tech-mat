# Virtual Garage Warehouse — Read-Only

## Purpose
Expose a read-only view of all vehicle builds, snapshots, and history.

---

## Scope

The Warehouse provides:
- Snapshot timelines
- Snapshot metadata
- Render / export availability
- Audit visibility (summary level)

The Warehouse does NOT allow:
- Editing
- Draft creation
- Snapshot finalization
- Tool execution

---

## Entities

### WarehouseItem
Represents a snapshot of a vehicle build.

Fields:
- snapshot_id
- project_id
- status (draft | completed | failed)
- created_at
- created_by
- parent_snapshot_id (nullable)
- engine_version
- has_render (bool)
- has_exports (bool)

---

## API Endpoints (Read-Only)

GET /warehouse/projects
GET /warehouse/projects/{project_id}
GET /warehouse/projects/{project_id}/snapshots

---

## Permissions

- viewer → allowed
- editor → allowed
- owner → allowed
- admin → allowed

---

## Forbidden

- Any mutation endpoint
- Any implicit draft creation
- Any tool execution
- Any station or mode changes

---

## Invariants

- Warehouse views reflect kernel truth
- Snapshot ordering is deterministic
- Drafts are clearly labeled
- Completed snapshots are immutable

