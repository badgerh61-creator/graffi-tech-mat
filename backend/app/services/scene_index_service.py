from __future__ import annotations

from typing import Any, Dict, List


def _default_stub_objects() -> List[Dict[str, Any]]:
    # Deterministic fallback until real asset registry / scene persistence exists.
    return [
        {
            "id": "vehicle-1",
            "kind": "vehicle",
            "name": "Default Vehicle",
            "asset_ref": "vehicles/default.glb",
            "transform": {
                "position": {"x": 0, "y": 0, "z": 0},
                "rotation": {"x": 0, "y": 0, "z": 0},
                "scale": {"x": 1, "y": 1, "z": 1},
            },
        }
    ]


def build_scene_index(snapshot: Any) -> Dict[str, Any]:
    """
    Deterministic scene index builder.

    Uses snapshot.body_state as the current best-known payload source.
    Accepts any of these future shapes (additive, safe):
      - body_state["scene"]["objects"]
      - body_state["objects"]

    If missing, returns a deterministic stub.
    """
    body = getattr(snapshot, "body_state", None) or {}

    # Shape A: { scene: { objects: [...] } }
    scene = body.get("scene")
    if isinstance(scene, dict):
        objs = scene.get("objects")
        if isinstance(objs, list):
            safe = [o for o in objs if isinstance(o, dict)]
            return {"snapshot_id": snapshot.id, "objects": safe}

    # Shape B: { objects: [...] }
    objs = body.get("objects")
    if isinstance(objs, list):
        safe = [o for o in objs if isinstance(o, dict)]
        return {"snapshot_id": snapshot.id, "objects": safe}

    return {"snapshot_id": snapshot.id, "objects": _default_stub_objects()}
