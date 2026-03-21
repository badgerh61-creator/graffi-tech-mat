from __future__ import annotations
from typing import Any, Dict, List, Optional


# -------------------------------------------------------
# Helpers
# -------------------------------------------------------

def _ensure_body(snapshot) -> Dict[str, Any]:
    body = getattr(snapshot, "body_state", None) or {}
    if not isinstance(body, dict):
        body = {}
    if "objects" not in body or not isinstance(body.get("objects"), list):
        body["objects"] = []
    return body


def _sorted_objects(objs: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    return sorted(objs, key=lambda o: str(o.get("id")))


def _find_object(objs: List[Dict[str, Any]], object_id: str) -> Optional[Dict[str, Any]]:
    for obj in objs:
        if isinstance(obj, dict) and str(obj.get("id")) == str(object_id):
            return obj
    return None


def _num(v: Any, fallback: float = 0.0) -> float:
    try:
        n = float(v)
        if n != n or n in (float("inf"), float("-inf")):
            return float(fallback)
        return n
    except Exception:
        return float(fallback)


def _bump_version(obj: Dict[str, Any]) -> int:
    return int(obj.get("version") or 0) + 1


# -------------------------------------------------------
# Pivot / Origin Editing
# -------------------------------------------------------

def validate_set_object_pivot(payload: Dict[str, Any]) -> Optional[str]:
    object_id = str(payload.get("object_id") or "").strip()
    if not object_id:
        return "object_id required"

    pivot = payload.get("pivot")
    if not isinstance(pivot, dict):
        return "pivot required"

    for k in ("x", "y", "z"):
        if k not in pivot:
            return f"pivot.{k} required"

    return None


def apply_set_object_pivot(snapshot, payload: Dict[str, Any]) -> Dict[str, Any]:
    body = _ensure_body(snapshot)
    objs = body["objects"]

    object_id = str(payload.get("object_id"))
    obj = _find_object(objs, object_id)
    if not obj:
        return {"ok": False, "error": "object not found"}

    pivot = payload.get("pivot") or {}

    obj["pivot"] = {
        "x": _num(pivot.get("x")),
        "y": _num(pivot.get("y")),
        "z": _num(pivot.get("z")),
    }

    obj["version"] = _bump_version(obj)

    body["objects"] = _sorted_objects(objs)
    setattr(snapshot, "body_state", body)

    return {"ok": True, "object_id": object_id, "pivot": obj["pivot"]}


def validate_reset_object_pivot(payload: Dict[str, Any]) -> Optional[str]:
    object_id = str(payload.get("object_id") or "").strip()
    if not object_id:
        return "object_id required"
    return None


def apply_reset_object_pivot(snapshot, payload: Dict[str, Any]) -> Dict[str, Any]:
    body = _ensure_body(snapshot)
    objs = body["objects"]

    object_id = str(payload.get("object_id"))
    obj = _find_object(objs, object_id)
    if not obj:
        return {"ok": False, "error": "object not found"}

    obj["pivot"] = None
    obj["version"] = _bump_version(obj)

    body["objects"] = _sorted_objects(objs)
    setattr(snapshot, "body_state", body)

    return {"ok": True, "object_id": object_id}


def validate_set_object_pivot_preset(payload: Dict[str, Any]) -> Optional[str]:
    object_id = str(payload.get("object_id") or "").strip()
    if not object_id:
        return "object_id required"

    preset = str(payload.get("preset") or "").strip()
    if preset not in ("center", "bounds_bottom_center"):
        return "preset invalid"

    pivot = payload.get("pivot")
    if not isinstance(pivot, dict):
        return "pivot required"

    for k in ("x", "y", "z"):
        if k not in pivot:
            return f"pivot.{k} required"

    return None


def apply_set_object_pivot_preset(snapshot, payload: Dict[str, Any]) -> Dict[str, Any]:
    body = _ensure_body(snapshot)
    objs = body["objects"]

    object_id = str(payload.get("object_id"))
    preset = str(payload.get("preset"))

    obj = _find_object(objs, object_id)
    if not obj:
        return {"ok": False, "error": "object not found"}

    pivot = payload.get("pivot") or {}

    obj["pivot"] = {
        "x": _num(pivot.get("x")),
        "y": _num(pivot.get("y")),
        "z": _num(pivot.get("z")),
    }

    obj["version"] = _bump_version(obj)

    body["objects"] = _sorted_objects(objs)
    setattr(snapshot, "body_state", body)

    return {
        "ok": True,
        "object_id": object_id,
        "preset": preset,
        "pivot": obj["pivot"],
    }
    
    
# -------------------------------------------------------
# Bulk Transform (Tier 7.63)
# -------------------------------------------------------

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


def validate_bulk_transform(payload: Dict[str, Any]) -> Optional[str]:
    object_ids = payload.get("object_ids")
    if not isinstance(object_ids, list) or not object_ids:
        return "object_ids required"

    mode = payload.get("mode")
    if mode not in ("translate", "rotate", "scale"):
        return "invalid mode"

    delta = payload.get("delta")
    if not isinstance(delta, dict):
        return "delta required"

    return None


def apply_bulk_transform(snapshot, payload: Dict[str, Any]) -> Dict[str, Any]:
    body = _ensure_body(snapshot)
    objs: List[Dict[str, Any]] = body["objects"]

    object_ids = set(_normalize_object_ids(payload.get("object_ids")))
    mode = payload.get("mode")
    delta = payload.get("delta") or {}

    updated = 0

    for obj in objs:
        oid = str(obj.get("id"))
        if oid not in object_ids:
            continue

        t = obj.get("transform") or {}

        pos = dict(t.get("pos") or {"x": 0, "y": 0, "z": 0})
        rot = dict(t.get("rot") or {"x": 0, "y": 0, "z": 0})
        scale = dict(t.get("scale") or {"x": 1, "y": 1, "z": 1})

        if mode == "translate" and "pos" in delta:
            d = delta.get("pos") or {}
            pos["x"] = _num(pos.get("x")) + _num(d.get("x"))
            pos["y"] = _num(pos.get("y")) + _num(d.get("y"))
            pos["z"] = _num(pos.get("z")) + _num(d.get("z"))

        elif mode == "rotate" and "rot" in delta:
            d = delta.get("rot") or {}
            rot["x"] = _num(rot.get("x")) + _num(d.get("x"))
            rot["y"] = _num(rot.get("y")) + _num(d.get("y"))
            rot["z"] = _num(rot.get("z")) + _num(d.get("z"))

        elif mode == "scale" and "scale" in delta:
            d = delta.get("scale") or {}
            scale["x"] = _num(scale.get("x"), 1) * _num(d.get("x"), 1)
            scale["y"] = _num(scale.get("y"), 1) * _num(d.get("y"), 1)
            scale["z"] = _num(scale.get("z"), 1) * _num(d.get("z"), 1)

        obj["transform"] = {
            "pos": pos,
            "rot": rot,
            "scale": scale,
        }

        obj["version"] = _bump_version(obj)
        updated += 1

    body["objects"] = _sorted_objects(objs)
    setattr(snapshot, "body_state", body)

    return {
        "ok": True,
        "updated": updated,
        "mode": mode,
    }  
    
# -------------------------------------------------------
# Numeric Transform (Tier 7.68)
# -------------------------------------------------------

def validate_set_object_transform(payload: Dict[str, Any]) -> Optional[str]:
    object_id = str(payload.get("object_id") or "").strip()
    if not object_id:
        return "object_id required"

    t = payload.get("transform")
    if not isinstance(t, dict):
        return "transform required"

    return None


def apply_set_object_transform(snapshot, payload: Dict[str, Any]) -> Dict[str, Any]:
    body = _ensure_body(snapshot)
    objs = body["objects"]

    object_id = str(payload.get("object_id"))
    obj = _find_object(objs, object_id)
    if not obj:
        return {"ok": False, "error": "object not found"}

    t = payload.get("transform") or {}

    obj["transform"] = {
        "pos": {
            "x": _num(t.get("pos", {}).get("x")),
            "y": _num(t.get("pos", {}).get("y")),
            "z": _num(t.get("pos", {}).get("z")),
        },
        "rot": {
            "x": _num(t.get("rot", {}).get("x")),
            "y": _num(t.get("rot", {}).get("y")),
            "z": _num(t.get("rot", {}).get("z")),
        },
        "scale": {
            "x": _num(t.get("scale", {}).get("x"), 1),
            "y": _num(t.get("scale", {}).get("y"), 1),
            "z": _num(t.get("scale", {}).get("z"), 1),
        },
    }

    obj["version"] = _bump_version(obj)

    body["objects"] = _sorted_objects(objs)
    setattr(snapshot, "body_state", body)

    return {"ok": True, "object_id": object_id}


def validate_bulk_offset_transform(payload: Dict[str, Any]) -> Optional[str]:
    if not isinstance(payload.get("object_ids"), list) or not payload.get("object_ids"):
        return "object_ids required"

    if not isinstance(payload.get("delta"), dict):
        return "delta required"

    return None


def apply_bulk_offset_transform(snapshot, payload: Dict[str, Any]) -> Dict[str, Any]:
    body = _ensure_body(snapshot)
    objs = body["objects"]

    ids = set(_normalize_object_ids(payload.get("object_ids")))
    delta = payload.get("delta") or {}

    def add_vec(base, d):
        return {
            "x": _num(base.get("x")) + _num(d.get("x")),
            "y": _num(base.get("y")) + _num(d.get("y")),
            "z": _num(base.get("z")) + _num(d.get("z")),
        }

    updated = 0

    for obj in objs:
        if obj.get("id") not in ids:
            continue

        t = obj.get("transform") or {}

        obj["transform"] = {
            "pos": add_vec(t.get("pos", {}), delta.get("pos", {})),
            "rot": add_vec(t.get("rot", {}), delta.get("rot", {})),
            "scale": add_vec(t.get("scale", {}), delta.get("scale", {})),
        }

        obj["version"] = _bump_version(obj)
        updated += 1

    body["objects"] = _sorted_objects(objs)
    setattr(snapshot, "body_state", body)

    return {"ok": True, "updated": updated}      
