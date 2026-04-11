from __future__ import annotations

from typing import Any, Dict, List, Optional


# --------------------------------------------------
# DEFAULT FALLBACK
# --------------------------------------------------

def _default_stub_objects() -> List[Dict[str, Any]]:
    return [
        {
            "id": "vehicle-1",
            "kind": "vehicle",
            "name": "Default Vehicle",
            "asset_ref": None,
            "parent_id": None,
            "material_state": {},
            "decal_state": [],
            "mesh_roles": {},
            "transform": {
                "position": {"x": 0, "y": 0, "z": 0},
                "rotation": {"x": 0, "y": 0, "z": 0},
                "scale": {"x": 1, "y": 1, "z": 1},
            },
        }
    ]


# --------------------------------------------------
# TRANSFORM
# --------------------------------------------------

def _normalize_transform(node: Dict[str, Any]) -> Dict[str, Any]:
    t = node.get("transform", {}) or {}

    return {
        "position": {
            "x": float(t.get("position", {}).get("x", 0)),
            "y": float(t.get("position", {}).get("y", 0)),
            "z": float(t.get("position", {}).get("z", 0)),
        },
        "rotation": {
            "x": float(t.get("rotation", {}).get("x", 0)),
            "y": float(t.get("rotation", {}).get("y", 0)),
            "z": float(t.get("rotation", {}).get("z", 0)),
        },
        "scale": {
            "x": float(t.get("scale", {}).get("x", 1)),
            "y": float(t.get("scale", {}).get("y", 1)),
            "z": float(t.get("scale", {}).get("z", 1)),
        },
    }


# --------------------------------------------------
# ASSET BINDING
# --------------------------------------------------

def _bind_asset(node: Dict[str, Any]) -> Optional[str]:
    asset_ref = node.get("asset_ref") or node.get("asset_id")

    if isinstance(asset_ref, str) and asset_ref.startswith("asset:"):
        return asset_ref

    if isinstance(asset_ref, int):
        return f"asset:{asset_ref}"

    return None


# --------------------------------------------------
# EXTRACTORS
# --------------------------------------------------

def _extract_material_state(node: Dict[str, Any]) -> Dict[str, Any]:
    ms = node.get("material_state") or {}
    return ms if isinstance(ms, dict) else {}


def _extract_decal_state(node: Dict[str, Any]) -> List[Dict[str, Any]]:
    ds = node.get("decal_state") or []
    return ds if isinstance(ds, list) else []


def _extract_mesh_roles(node: Dict[str, Any]) -> Dict[str, Any]:
    roles = node.get("mesh_roles") or {}
    return roles if isinstance(roles, dict) else {}


# --------------------------------------------------
# MATERIAL OVERRIDE (FULL FIX)
# --------------------------------------------------

def _resolve_overrides(snapshot: Any, body: Dict[str, Any]) -> Dict[str, Any]:
    # snapshot.decor_state.material_overrides
    decor = getattr(snapshot, "decor_state", None)
    if isinstance(decor, dict):
        mo = decor.get("material_overrides")
        if isinstance(mo, dict):
            return mo

    # body.decor_state.material_overrides
    decor = body.get("decor_state")
    if isinstance(decor, dict):
        mo = decor.get("material_overrides")
        if isinstance(mo, dict):
            return mo

    # body.decor.material_overrides
    decor = body.get("decor")
    if isinstance(decor, dict):
        mo = decor.get("material_overrides")
        if isinstance(mo, dict):
            return mo

    # body.scene.decor.material_overrides
    scene = body.get("scene")
    if isinstance(scene, dict):
        decor = scene.get("decor")
        if isinstance(decor, dict):
            mo = decor.get("material_overrides")
            if isinstance(mo, dict):
                return mo

    return {}


# --------------------------------------------------
# CORE BUILDER
# --------------------------------------------------

def _build_from_nodes(
    nodes: List[Dict[str, Any]],
    overrides: Dict[str, Any]
) -> List[Dict[str, Any]]:
    objects: List[Dict[str, Any]] = []

    # 🔥 support nested material_overrides
    if "material_overrides" in overrides:
        overrides = overrides.get("material_overrides", {})

    for n in nodes:
        if not isinstance(n, dict):
            continue

        obj_id = str(n.get("id") or "").strip()
        if not obj_id:
            continue

        parent_id = n.get("parent_id")
        if parent_id is not None:
            parent_id = str(parent_id)

        base_material = _extract_material_state(n)

        override = overrides.get(obj_id, {}) or {}
        params = override.get("params") if isinstance(override, dict) else None

        if params:
            material_state = {
                "paint": {
                    "color": params.get("color"),
                    "roughness": params.get("roughness"),
                    "metalness": params.get("metalness"),
                }
            }
        else:
            material_state = base_material

        obj = {
            "id": obj_id,
            "kind": n.get("kind", "node"),
            "name": n.get("name"),
            "asset_ref": _bind_asset(n),
            "parent_id": parent_id,
            "material_state": material_state,
            "decal_state": _extract_decal_state(n),
            "mesh_roles": _extract_mesh_roles(n),
            "transform": _normalize_transform(n),
        }

        objects.append(obj)

    return objects
    
# --------------------------------------------------
# PUBLIC API
# --------------------------------------------------

def build_scene_index(snapshot: Any) -> Dict[str, Any]:
    body = getattr(snapshot, "body_state", None) or {}

    # 🔥 read decor_state directly
    decor = getattr(snapshot, "decor_state", {}) or {}
    overrides = decor.get("material_overrides", {})

    scene = body.get("scene") or {}

    nodes = (
        scene.get("nodes")
        or scene.get("objects")
        or body.get("nodes")
        or body.get("objects")
        or []
    )

    if isinstance(nodes, list):
        objects = _build_from_nodes(nodes, overrides)

        if objects:
            return {
                "snapshot_id": snapshot.id,
                "objects": objects,
            }

    return {
        "snapshot_id": snapshot.id,
        "objects": _default_stub_objects(),
    }
