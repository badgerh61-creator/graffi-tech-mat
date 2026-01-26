# backend/app/services/__init__.py

from . import thumbnails
from .export_service import export_snapshot
from app.services.snapshot_finalize import finalize_snapshot

# Phase 5.1 — snapshot transform primitive
from app.services.snapshot_mutations import apply_transform

from app.services.snapshot_navigation import (
    undo_snapshot,
    redo_snapshot,
 )
    
# 🔹 Phase J.3 — constraint solving
from app.services.constraint_solver import solve_constraints   

# Phase K.1 — surface generation
from app.services.surface_generation_service import generate_surfaces_for_snapshot

# Phase K.2 — panel segmentation
from app.services.panel_segmenter import segment_panels

# Phase K.3 — panel parameters
from app.services.panel_parameters import apply_panel_parameters

__all__ = [
    "thumbnails",
    "export_snapshot",
    "finalize_snapshot",
    "apply_transform",
    "undo_snapshot",
    "redo_snapshot",
    "solve_constraints",
    "generate_surfaces_for_snapshot",
    "segment_panels",
    "apply_panel_parameters",
]


