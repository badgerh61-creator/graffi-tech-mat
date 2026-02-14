# backend/app/services/__init__.py
# Barrel exports ONLY — no logic allowed here

# Core
from . import thumbnails
from .export_service import export_snapshot
from .snapshot_finalize import finalize_snapshot

# Phase 5 — Snapshot mutations
from .snapshot_mutations import apply_transform
from .snapshot_navigation import undo_snapshot, redo_snapshot

# Phase J / K — Geometry
from .constraint_solver import solve_constraints
from .surface_generation_service import generate_surfaces_for_snapshot
from .panel_segmenter import segment_panels
from .panel_parameters import apply_panel_parameters

# Phase R — AI
from .ai_assistant import AssistantService
from .ai_proposals import request_ai_proposal

# Phase U.3 — Conflict system
from .conflict_detector import detect_conflict, ConflictResult
from .conflict_resolver import resolve_conflict, resolve_conflict_and_fork

# Phase U.1 — Sessions
from .session_service import start_session, end_session

# Phase U.2 — Draft ownership
from .draft_lock_service import (
    acquire_draft_lock,
    release_draft_lock,
    get_draft_lock,
    require_draft_owner,
)

# Phase U.5 — Read views
from .read_view_service import open_read_view
from .read_view_guard import has_active_read_view, reject_mutation_from_read_view


__all__ = [
    # Core
    "thumbnails",
    "export_snapshot",
    "finalize_snapshot",

    # Phase 5
    "apply_transform",
    "undo_snapshot",
    "redo_snapshot",

    # Phase J / K
    "solve_constraints",
    "generate_surfaces_for_snapshot",
    "segment_panels",
    "apply_panel_parameters",

    # Phase R
    "AssistantService",
    "request_ai_proposal",

    # Phase U.3
    "detect_conflict",
    "ConflictResult",
    "resolve_conflict",
    "resolve_conflict_and_fork",

    # Phase U.1
    "start_session",
    "end_session",

    # Phase U.2
    "acquire_draft_lock",
    "release_draft_lock",
    "get_draft_lock",
    "require_draft_owner",

    # Phase U.5
    "open_read_view",
    "has_active_read_view",
    "reject_mutation_from_read_view", 

]

