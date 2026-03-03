from __future__ import annotations

from typing import Any, Dict, List, Optional
import uuid


def _ensure_body(snapshot) -> Dict[str, Any]:
    body = getattr(snapshot, "body_state", None) or {}
    if not isinstance(body, dict):
        body = {}
    if "objects" not in body or not isinstance(body.get("objects"), list):
        body["objects"] = []
    return body


def _default_transform() -> Dict[str, Any]:
    return {
        "pos": {"x": 0, "y": 0, "z": 0},
        "rot": {"x": 0, "y": 0, "z": 0},  # degrees
        "scale": {"x": 1, "y": 1, "z": 1},
    }


def validate_add_model_ref(params: Dict[str, Any]) -> Optional[str]:
    asset_id = params.get("asset_id")
    if asset_id is None:
        return "asset_id required"
    try:
        int(asset_id)
    except Exception:
        return "asset_id must be int"
    return None


def validate_remove_object(params: Dict[str, Any]) -> Optional[str]:
    oid = str(params.get("object_id") or "").strip()
    if not oid:
        return "object_id required"
    return None


def apply_add_model_ref(snapshot, params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Store model reference in snapshot.body_state.objects (authoritative).
    asset_id refers to Asset table id (DB-backed, permission-checked elsewhere).
    """
    body = _ensure_body(snapshot)
    objs: List[Dict[str, Any]] = body["objects"]

    asset_id = int(params.get("asset_id"))
    name = str(params.get("name") or f"Asset {asset_id}")
    transform = params.get("transform") or _default_transform()

    oid = f"obj-{uuid.uuid4().hex[:12]}"

    objs.append(
        {
            "id": oid,
            "kind": "model_ref",
            "name": name,
            "asset_id": asset_id,
            "transform": transform,
            "layers": ["default"],
            "enabled": True,
            "version": 1,
        }
    )

    body["objects"] = sorted(objs, key=lambda o: str(o.get("id")))
    setattr(snapshot, "body_state", body)

    return {"ok": True, "object_id": oid, "asset_id": asset_id}


def apply_remove_object(snapshot, params: Dict[str, Any]) -> Dict[str, Any]:
    body = _ensure_body(snapshot)
    objs: List[Dict[str, Any]] = body["objects"]

    oid = str(params.get("object_id"))
    before = len(objs)
    objs2 = [o for o in objs if str(o.get("id")) != oid]
    removed = before - len(objs2)

    body["objects"] = sorted(objs2, key=lambda o: str(o.get("id")))
    setattr(snapshot, "body_state", body)

    return {"ok": True, "removed": removed, "object_id": oid}
