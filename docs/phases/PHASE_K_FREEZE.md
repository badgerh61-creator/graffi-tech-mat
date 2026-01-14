# Phase K Freeze — Deterministic Mutations & Snapshots

## Scope (Frozen)
Phase K establishes deterministic, immutable mutation behavior via
snapshot cloning and journaling.

This phase includes:
- Decor mutations (Phase K.1)
- Tuning mutations (Phase K.2)
- Router-level capability normalization
- Deterministic snapshot hashing
- Journal-backed mutation history

## Invariants (DO NOT CHANGE)
- Mutations never mutate base snapshots
- Snapshot identity is derived from deterministic hashes
- All mutations write journal entries
- Capability enforcement occurs at router level
- Services remain side-effect free beyond snapshot creation

## Explicitly Frozen Files
- app/api/mutations/decor/**
- app/api/mutations/tuning/**
- app/models/rendered_snapshot.py
- app/models/journal_entry.py

## Allowed After Freeze
- Read-only consumption of snapshots
- UI/editor integration (Phase L)
- Snapshot switching (undo/redo)
- Schema / CRUD *segmentation only* (no behavior changes)

## Forbidden After Freeze
- New mutation types
- Snapshot schema changes
- Journal semantics changes
- Capability logic changes

Frozen on: 2026-01-14

