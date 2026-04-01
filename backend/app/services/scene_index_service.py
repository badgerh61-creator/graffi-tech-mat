from __future__ import annotations

from typing import Any, Dict, List


def _default_stub_objects() -> List[Dict[str, Any]]:
    """
    Deterministic fallback when no scene data exists.
    MUST NOT pretend a real asset exists.
    """
    return [
        {
            "id": "vehicle-1",
            "kind": "vehicle",
            "name": "Default Vehicle",
            "asset_ref": None,
            "transform": {
                "position": {"x": 0, "y": 0, "z": 0},
                "rotation": {"x": 0, "y": 0, "z": 0},
                "scale": {"x": 1, "y": 1, "z": 1},
            },
        }
    ]


def _normalize_transform(node: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "position": node.get("transform", {}).get(
            "position", {"x": 0, "y": 0, "z": 0}
        ),
        "rotation": node.get("transform", {}).get(
            "rotation", {"x": 0, "y": 0, "z": 0}
        ),
        "scale": node.get("transform", {}).get(
            "scale", {"x": 1, "y": 1, "z": 1}
        ),
    }


def _bind_asset(node: Dict[str, Any]) -> str | None:
    """
    Tier 6G.13 — Correct binding:
    Accept BOTH:
    - int → "asset:<id>"
    - "asset:<id>" → pass through
    """
    asset_ref = node.get("asset_ref")

    # ✅ already correct format
    if isinstance(asset_ref, str) and asset_ref.startswith("asset:"):
        return asset_ref

    # ✅ legacy int support
    if isinstance(asset_ref, int):
        return f"asset:{asset_ref}"

    return None
    

def _build_from_nodes(nodes: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    objects = []

    for n in nodes:
        if not isinstance(n, dict):
            continue

        obj_id = str(n.get("id") or "").strip()
        if not obj_id:
            continue

        objects.append(
            {
                "id": obj_id,
                "kind": n.get("kind", "node"),
                "name": n.get("name"),
                "asset_ref": _bind_asset(n),  # ✅ FIXED
                "transform": _normalize_transform(n),
            }
        )

    return objects


def build_scene_index(snapshot: Any) -> Dict[str, Any]:
    """
    Tier 6G.13 — Real Asset Binding Scene Index

    Rules:
    - Deterministic
    - Read-only
    - No DB access
    - asset_ref → viewer binding happens here ONLY
    """

    body = getattr(snapshot, "body_state", None) or {}

    # ✅ Preferred shape (future-safe)
    scene = body.get("scene")
    if isinstance(scene, dict):
        nodes = scene.get("nodes") or scene.get("objects")
        if isinstance(nodes, list):
            objects = _build_from_nodes(nodes)
            if objects:
                return {"snapshot_id": snapshot.id, "objects": objects}

    # ✅ Flat fallback
    nodes = body.get("nodes") or body.get("objects")
    if isinstance(nodes, list):
        objects = _build_from_nodes(nodes)
        if objects:
            return {"snapshot_id": snapshot.id, "objects": objects}

    # ❌ Nothing usable → deterministic stub
    return {
        "snapshot_id": snapshot.id,
        "objects": _default_stub_objects(),
    }
