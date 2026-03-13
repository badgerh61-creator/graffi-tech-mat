from __future__ import annotations

from typing import Any, Dict, List, Optional
import copy
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


def _find_object(objs: List[Dict[str, Any]], object_id: str) -> Optional[Dict[str, Any]]:
    for obj in objs:
        if isinstance(obj, dict) and str(obj.get("id")) == str(object_id):
            return obj
    return None


def _sorted_objects(objs: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    return sorted(objs, key=lambda o: str(o.get("id")))


def _make_object_id() -> str:
    return f"obj-{uuid.uuid4().hex[:12]}"


def _num(v: Any, fallback: float = 0.0) -> float:
    try:
        return float(v)
    except Exception:
        return float(fallback)


def _normalize_object_ids(ids) -> List[str]:
    seen = set()
    out = []
    for raw in ids or []:
        s = str(raw or "").strip()
        if not s or s in seen:
            continue
        seen.add(s)
        out.append(s)
    return out


def _would_create_cycle(objs: List[Dict[str, Any]], object_id: str, parent_id: str) -> bool:
    current = _find_object(objs, parent_id)
    seen = set()

    while current:
        cid = str(current.get("id"))
        if cid == str(object_id):
            return True
        if cid in seen:
            return True
        seen.add(cid)

        next_parent = current.get("parent_id")
        if not next_parent:
            return False
        current = _find_object(objs, str(next_parent))

    return False


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


def validate_set_object_enabled(params: Dict[str, Any]) -> Optional[str]:
    oid = str(params.get("object_id") or "").strip()
    if not oid:
        return "object_id required"
    if not isinstance(params.get("enabled"), bool):
        return "enabled must be boolean"
    return None


def validate_set_object_layers(params: Dict[str, Any]) -> Optional[str]:
    oid = str(params.get("object_id") or "").strip()
    if not oid:
        return "object_id required"

    layers = params.get("layers")
    if not isinstance(layers, list):
        return "layers must be a list"

    for layer in layers:
        if not str(layer).strip():
            return "layers must contain non-empty strings"

    return None


def validate_duplicate_object(params: Dict[str, Any]) -> Optional[str]:
    oid = str(params.get("object_id") or "").strip()
    if not oid:
        return "object_id required"

    offset = params.get("offset", None)
    if offset is not None and not isinstance(offset, dict):
        return "offset must be an object"

    return None


def validate_mirror_object(params: Dict[str, Any]) -> Optional[str]:
    oid = str(params.get("object_id") or "").strip()
    if not oid:
        return "object_id required"

    axis = str(params.get("axis") or "").lower()
    if axis not in ("x", "y", "z"):
        return "axis must be x, y, or z"

    return None


def validate_create_group(params: Dict[str, Any]) -> Optional[str]:
    name = str(params.get("name") or "").strip()
    if not name:
        return "name required"
    return None


def validate_parent_object(params: Dict[str, Any]) -> Optional[str]:
    object_id = str(params.get("object_id") or "").strip()
    parent_id = str(params.get("parent_id") or "").strip()

    if not object_id:
        return "object_id required"
    if not parent_id:
        return "parent_id required"
    if object_id == parent_id:
        return "object cannot parent to itself"

    return None


def validate_unparent_object(params: Dict[str, Any]) -> Optional[str]:
    object_id = str(params.get("object_id") or "").strip()
    if not object_id:
        return "object_id required"
    return None


def validate_bulk_set_enabled(params: Dict[str, Any]) -> Optional[str]:
    object_ids = params.get("object_ids")
    if not isinstance(object_ids, list) or not object_ids:
        return "object_ids must be a non-empty list"
    if not isinstance(params.get("enabled"), bool):
        return "enabled must be boolean"
    return None


def validate_bulk_set_layers(params: Dict[str, Any]) -> Optional[str]:
    object_ids = params.get("object_ids")
    if not isinstance(object_ids, list) or not object_ids:
        return "object_ids must be a non-empty list"

    layers = params.get("layers")
    if not isinstance(layers, list):
        return "layers must be a list"

    for layer in layers:
        if not str(layer).strip():
            return "layers must contain non-empty strings"

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

    oid = _make_object_id()

    objs.append(
        {
            "id": oid,
            "kind": "model_ref",
            "name": name,
            "asset_id": asset_id,
            "parent_id": None,
            "transform": transform,
            "layers": ["default"],
            "enabled": True,
            "version": 1,
        }
    )

    body["objects"] = _sorted_objects(objs)
    setattr(snapshot, "body_state", body)

    return {"ok": True, "object_id": oid, "asset_id": asset_id}


def apply_remove_object(snapshot, params: Dict[str, Any]) -> Dict[str, Any]:
    body = _ensure_body(snapshot)
    objs: List[Dict[str, Any]] = body["objects"]

    oid = str(params.get("object_id"))
    before = len(objs)
    objs2 = [o for o in objs if str(o.get("id")) != oid]
    removed = before - len(objs2)

    body["objects"] = _sorted_objects(objs2)
    setattr(snapshot, "body_state", body)

    return {"ok": True, "removed": removed, "object_id": oid}


def apply_set_object_enabled(snapshot, params: Dict[str, Any]) -> Dict[str, Any]:
    body = _ensure_body(snapshot)
    objs: List[Dict[str, Any]] = body["objects"]

    oid = str(params.get("object_id"))
    enabled = bool(params.get("enabled"))

    obj = _find_object(objs, oid)
    if not obj:
        return {"ok": False, "error": "object not found"}

    obj["enabled"] = enabled
    obj["version"] = int(obj.get("version") or 1)

    body["objects"] = _sorted_objects(objs)
    setattr(snapshot, "body_state", body)

    return {"ok": True, "object_id": oid, "enabled": enabled}


def apply_set_object_layers(snapshot, params: Dict[str, Any]) -> Dict[str, Any]:
    body = _ensure_body(snapshot)
    objs: List[Dict[str, Any]] = body["objects"]

    oid = str(params.get("object_id"))
    layers = sorted({str(x) for x in (params.get("layers") or []) if str(x).strip()})

    obj = _find_object(objs, oid)
    if not obj:
        return {"ok": False, "error": "object not found"}

    obj["layers"] = layers or ["default"]
    obj["version"] = int(obj.get("version") or 1)

    body["objects"] = _sorted_objects(objs)
    setattr(snapshot, "body_state", body)

    return {"ok": True, "object_id": oid, "layers": obj["layers"]}


def apply_duplicate_object(snapshot, params: Dict[str, Any]) -> Dict[str, Any]:
    body = _ensure_body(snapshot)
    objs: List[Dict[str, Any]] = body["objects"]

    oid = str(params.get("object_id"))
    src = _find_object(objs, oid)
    if not src:
        return {"ok": False, "error": "object not found"}

    offset = params.get("offset") or {}
    dx = _num(offset.get("x", 0))
    dy = _num(offset.get("y", 0))
    dz = _num(offset.get("z", 0))

    clone = copy.deepcopy(src)
    clone["id"] = _make_object_id()
    clone["name"] = f'{str(src.get("name") or src.get("id") or "Object")} Copy'
    clone["version"] = 1

    transform = clone.get("transform") or {}
    pos = transform.get("pos") or {"x": 0, "y": 0, "z": 0}

    pos["x"] = _num(pos.get("x", 0)) + dx
    pos["y"] = _num(pos.get("y", 0)) + dy
    pos["z"] = _num(pos.get("z", 0)) + dz

    transform["pos"] = pos
    clone["transform"] = transform

    objs.append(clone)
    body["objects"] = _sorted_objects(objs)
    setattr(snapshot, "body_state", body)

    return {"ok": True, "object_id": clone["id"], "source_object_id": oid}


def apply_mirror_object(snapshot, params: Dict[str, Any]) -> Dict[str, Any]:
    body = _ensure_body(snapshot)
    objs: List[Dict[str, Any]] = body["objects"]

    oid = str(params.get("object_id"))
    axis = str(params.get("axis")).lower()

    src = _find_object(objs, oid)
    if not src:
        return {"ok": False, "error": "object not found"}

    clone = copy.deepcopy(src)
    clone["id"] = _make_object_id()
    clone["name"] = f'{str(src.get("name") or src.get("id") or "Object")} Mirror'
    clone["version"] = 1

    transform = clone.get("transform") or {}
    pos = transform.get("pos") or {"x": 0, "y": 0, "z": 0}

    pos[axis] = -_num(pos.get(axis, 0))
    transform["pos"] = pos
    clone["transform"] = transform

    objs.append(clone)
    body["objects"] = _sorted_objects(objs)
    setattr(snapshot, "body_state", body)

    return {
        "ok": True,
        "object_id": clone["id"],
        "source_object_id": oid,
        "axis": axis,
    }


def apply_create_group(snapshot, params: Dict[str, Any]) -> Dict[str, Any]:
    body = _ensure_body(snapshot)
    objs: List[Dict[str, Any]] = body["objects"]

    oid = _make_object_id()
    name = str(params.get("name") or "Group")

    objs.append(
        {
            "id": oid,
            "kind": "group",
            "name": name,
            "asset_id": None,
            "parent_id": None,
            "transform": _default_transform(),
            "layers": ["default"],
            "enabled": True,
            "version": 1,
        }
    )

    body["objects"] = _sorted_objects(objs)
    setattr(snapshot, "body_state", body)
    return {"ok": True, "object_id": oid}


def apply_parent_object(snapshot, params: Dict[str, Any]) -> Dict[str, Any]:
    body = _ensure_body(snapshot)
    objs: List[Dict[str, Any]] = body["objects"]

    object_id = str(params.get("object_id"))
    parent_id = str(params.get("parent_id"))

    obj = _find_object(objs, object_id)
    parent = _find_object(objs, parent_id)

    if not obj:
        return {"ok": False, "error": "object not found"}
    if not parent:
        return {"ok": False, "error": "parent not found"}
    if object_id == parent_id:
        return {"ok": False, "error": "object cannot parent to itself"}
    if _would_create_cycle(objs, object_id, parent_id):
        return {"ok": False, "error": "parenting would create cycle"}

    obj["parent_id"] = parent_id
    obj["version"] = int(obj.get("version") or 1)

    body["objects"] = _sorted_objects(objs)
    setattr(snapshot, "body_state", body)
    return {"ok": True, "object_id": object_id, "parent_id": parent_id}


def apply_unparent_object(snapshot, params: Dict[str, Any]) -> Dict[str, Any]:
    body = _ensure_body(snapshot)
    objs: List[Dict[str, Any]] = body["objects"]

    object_id = str(params.get("object_id"))
    obj = _find_object(objs, object_id)

    if not obj:
        return {"ok": False, "error": "object not found"}

    obj["parent_id"] = None
    obj["version"] = int(obj.get("version") or 1)

    body["objects"] = _sorted_objects(objs)
    setattr(snapshot, "body_state", body)
    return {"ok": True, "object_id": object_id}


def apply_bulk_set_enabled(snapshot, params: Dict[str, Any]) -> Dict[str, Any]:
    body = _ensure_body(snapshot)
    objs: List[Dict[str, Any]] = body["objects"]

    object_ids = set(_normalize_object_ids(params.get("object_ids")))
    enabled = bool(params.get("enabled"))

    updated = 0
    for obj in objs:
        oid = str(obj.get("id"))
        if oid in object_ids:
            obj["enabled"] = enabled
            obj["version"] = int(obj.get("version") or 1)
            updated += 1

    body["objects"] = _sorted_objects(objs)
    setattr(snapshot, "body_state", body)
    return {"ok": True, "updated": updated, "enabled": enabled}


def apply_bulk_set_layers(snapshot, params: Dict[str, Any]) -> Dict[str, Any]:
    body = _ensure_body(snapshot)
    objs: List[Dict[str, Any]] = body["objects"]

    object_ids = set(_normalize_object_ids(params.get("object_ids")))
    layers = sorted({str(x) for x in (params.get("layers") or []) if str(x).strip()}) or ["default"]

    updated = 0
    for obj in objs:
        oid = str(obj.get("id"))
        if oid in object_ids:
            obj["layers"] = layers
            obj["version"] = int(obj.get("version") or 1)
            updated += 1

    body["objects"] = _sorted_objects(objs)
    setattr(snapshot, "body_state", body)
    return {"ok": True, "updated": updated, "layers": layers}
