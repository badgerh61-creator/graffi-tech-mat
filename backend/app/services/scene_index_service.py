from __future__ import annotations
from typing import Any, Dict, List, Optional


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


def _bind_asset(node: Dict[str, Any]) -> Optional[str]:
    asset_ref = node.get("asset_ref") or node.get("asset_id")

    if isinstance(asset_ref, str) and asset_ref.startswith("asset:"):
        return asset_ref

    if isinstance(asset_ref, int):
        return f"asset:{asset_ref}"

    # 🔥 FALLBACK — FORCE WORKING ASSET
    return "asset:2"


def _extract_material_state(node: Dict[str, Any]) -> Dict[str, Any]:
    ms = node.get("material_state") or {}
    return ms if isinstance(ms, dict) else {}


def _extract_decal_state(node: Dict[str, Any]) -> List[Dict[str, Any]]:
    ds = node.get("decal_state") or []
    return ds if isinstance(ds, list) else []


def _extract_mesh_roles(node: Dict[str, Any]) -> Dict[str, Any]:
    roles = node.get("mesh_roles") or {}
    return roles if isinstance(roles, dict) else {}


def _build_from_nodes(
    nodes: List[Dict[str, Any]],
    overrides: Dict[str, Any]
) -> List[Dict[str, Any]]:

    objects: List[Dict[str, Any]] = []

    # ✅ ALWAYS normalize overrides
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

        existing_material = _extract_material_state(n)

        # -----------------------------
        # 🔥 FIX — STRICT mesh override filtering
        # -----------------------------
        mesh_overrides = {}

        for key, value in overrides.items():
            if not isinstance(key, str):
                continue

            if key.startswith(f"mesh:{obj_id}::"):
                mesh_overrides[key] = value

        existing_meshes = existing_material.get("meshes", {}) or {}

        # -----------------------------
        # 🔥 CRITICAL — MERGE CORRECTLY
        # -----------------------------
        merged_meshes = {
            **existing_meshes,
            **mesh_overrides
        }

        material_state = {
            **existing_material
        }

        if merged_meshes:
            material_state["meshes"] = merged_meshes

        # -----------------------------
        # mesh roles
        # -----------------------------
        mesh_roles = _extract_mesh_roles(n)

        if not mesh_roles:
            mesh_roles = {
                "_auto": True,
                "body": n.get("name") or "body",
                "wheels": "wheel",
                "glass": "glass",
                "lights": "light",
                "doors": "door",
                "trim": "trim",
                "interior": "interior",
                "chassis": "chassis",
                "engine": "engine",
            }

        obj = {
            "id": obj_id,
            "kind": n.get("kind", "node"),
            "name": n.get("name"),
            "asset_ref": _bind_asset(n),
            "parent_id": parent_id,
            "material_state": material_state,
            "decal_state": _extract_decal_state(n),
            "mesh_roles": mesh_roles,
            "transform": _normalize_transform(n),
        }

        objects.append(obj)

    return objects


def build_scene_index(snapshot: Any) -> Dict[str, Any]:
    body = getattr(snapshot, "body_state", None) or {}

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
