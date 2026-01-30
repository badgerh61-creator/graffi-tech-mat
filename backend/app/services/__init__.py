# backend/app/services/__init__.py
# Barrel exports ONLY — no logic allowed here

from . import thumbnails
from .export_service import export_snapshot
from .snapshot_finalize import finalize_snapshot

# Phase 5
from .snapshot_mutations import apply_transform
from .snapshot_navigation import undo_snapshot, redo_snapshot

# Phase J / K
from .constraint_solver import solve_constraints
from .surface_generation_service import generate_surfaces_for_snapshot
from .panel_segmenter import segment_panels
from .panel_parameters import apply_panel_parameters

# Phase R
from .ai_assistant import AssistantService
from .ai_proposals import request_ai_proposal

# Phase U.3 — CONFLICT SYSTEM (AUTHORITATIVE)
from .conflict_detector import detect_conflict, ConflictResult
from .conflict_resolver import resolve_conflict, resolve_conflict_and_fork

__all__ = [
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

    # Phase U.3
    "detect_conflict",
    "ConflictResult",
    "resolve_conflict",
    "resolve_conflict_and_fork",

    # Phase R
    "AssistantService",
    "request_ai_proposal",
]

