from __future__ import annotations

from typing import Any, Dict, List


def compute_reference_frames_for_snapshot(*, snapshot) -> Dict[str, Any]:
    """
    Tier 7.2 — Read-only, deterministic reference frames.
    No DB writes, no mutation.
    """
    planes: List[Dict[str, Any]] = [
        {"id": "world_xy", "label": "World XY", "normal": [0, 0, 1], "origin": [0, 0, 0]},
        {"id": "world_yz", "label": "World YZ", "normal": [1, 0, 0], "origin": [0, 0, 0]},
        {"id": "world_xz", "label": "World XZ", "normal": [0, 1, 0], "origin": [0, 0, 0]},
    ]

    active_plane_id = "world_xy"
    if hasattr(snapshot, "active_plane_id") and getattr(snapshot, "active_plane_id"):
        active_plane_id = str(getattr(snapshot, "active_plane_id"))

    return {
        "snapshot_id": int(getattr(snapshot, "id")),
        "axes": {
            "x": {"label": "X", "unit": "m"},
            "y": {"label": "Y", "unit": "m"},
            "z": {"label": "Z", "unit": "m"},
        },
        "planes": planes,
        "defaults": {"active_plane_id": active_plane_id},
    }
