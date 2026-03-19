from __future__ import annotations
from typing import Any, Dict, List, Optional

# --- Material override imports / helpers ---
from app.services.materials.presets import is_valid_preset
from app.services.materials.params import validate_patch, clamp01, normalize_color

# --- Material override helpers ---
def _ensure_decor(snapshot) -> Dict[str, Any]:
    decor = getattr(snapshot, "decor_state", None) or {}
    if not isinstance(decor, dict):
        decor = {}
    if "material_overrides" not in decor or not isinstance(decor.get("material_overrides"), dict):
        decor["material_overrides"] = {}
    return decor

def _slot_key(target_id: str, slot_name: str) -> str:
    tid = str(target_id or "").strip()
    slot = str(slot_name or "").strip()
    return f"{tid}::slot:{slot}"

# --- Material override validators ---
def validate_set(payload: Dict[str, Any]) -> Optional[str]:
    tid = str(payload.get("target_id") or "").strip()
    if not tid:
        return "target_id required"

    preset = str(payload.get("preset") or "").strip()
    if not preset:
        return "preset required"
    if not is_valid_preset(preset):
        return "preset invalid"

    return None

def validate_clear(payload: Dict[str, Any]) -> Optional[str]:
    tid = str(payload.get("target_id") or "").strip()
    if not tid:
        return "target_id required"
    return None

def validate_update_params(payload: Dict[str, Any]) -> Optional[str]:
    tid = str(payload.get("target_id") or "").strip()
    if not tid:
        return "target_id required"

    patch = payload.get("patch")
    err = validate_patch(patch)
    if err:
        return err

    return None

def validate_set_slot(payload: Dict[str, Any]) -> Optional[str]:
    tid = str(payload.get("target_id") or "").strip()
    if not tid:
        return "target_id required"

    slot_name = str(payload.get("slot_name") or "").strip()
    if not slot_name:
        return "slot_name required"

    preset = str(payload.get("preset") or "").strip()
    if not preset:
        return "preset required"
    if not is_valid_preset(preset):
        return "preset invalid"

    return None

def validate_clear_slot(payload: Dict[str, Any]) -> Optional[str]:
    tid = str(payload.get("target_id") or "").strip()
    if not tid:
        return "target_id required"

    slot_name = str(payload.get("slot_name") or "").strip()
    if not slot_name:
        return "slot_name required"

    return None

# --- Material override appliers ---
def apply_set(snapshot, payload: Dict[str, Any]) -> Dict[str, Any]:
    decor = _ensure_decor(snapshot)
    overrides: Dict[str, Any] = decor["material_overrides"]

    tid = str(payload.get("target_id")).strip()
    preset = str(payload.get("preset")).strip()

    overrides[tid] = {
        "preset": preset,
        "params": {},
        "version": 1,
    }

    decor["material_overrides"] = overrides
    setattr(snapshot, "decor_state", decor)
    return {"ok": True, "target_id": tid, "preset": preset}

def apply_clear(snapshot, payload: Dict[str, Any]) -> Dict[str, Any]:
    decor = _ensure_decor(snapshot)
    overrides: Dict[str, Any] = decor["material_overrides"]

    tid = str(payload.get("target_id")).strip()
    if tid in overrides:
        del overrides[tid]

    decor["material_overrides"] = overrides
    setattr(snapshot, "decor_state", decor)
    return {"ok": True, "target_id": tid}

def apply_update_params(snapshot, payload: Dict[str, Any]) -> Dict[str, Any]:
    decor = _ensure_decor(snapshot)
    overrides: Dict[str, Any] = decor["material_overrides"]

    tid = str(payload.get("target_id")).strip()
    if tid not in overrides:
        return {"ok": False, "error": "override missing"}

    patch = payload.get("patch") or {}
    cur = overrides[tid]
    params = cur.get("params") or {}
    if not isinstance(params, dict):
        params = {}

    if "color" in patch:
        params["color"] = normalize_color(str(patch["color"]))

    for k in ("roughness", "metalness", "opacity"):
        if k in patch:
            params[k] = clamp01(float(patch[k]))

    cur["params"] = params
    cur["version"] = int(cur.get("version") or 1)

    overrides[tid] = cur
    decor["material_overrides"] = overrides
    setattr(snapshot, "decor_state", decor)

    return {"ok": True, "target_id": tid, "params": params}

def apply_set_slot(snapshot, payload: Dict[str, Any]) -> Dict[str, Any]:
    decor = _ensure_decor(snapshot)
    overrides: Dict[str, Any] = decor["material_overrides"]

    tid = str(payload.get("target_id")).strip()
    slot_name = str(payload.get("slot_name")).strip()
    preset = str(payload.get("preset")).strip()

    key = _slot_key(tid, slot_name)
    overrides[key] = {
        "preset": preset,
        "params": {},
        "version": 1,
    }

    decor["material_overrides"] = overrides
    setattr(snapshot, "decor_state", decor)
    return {"ok": True, "override_key": key, "preset": preset}

def apply_clear_slot(snapshot, payload: Dict[str, Any]) -> Dict[str, Any]:
    decor = _ensure_decor(snapshot)
    overrides: Dict[str, Any] = decor["material_overrides"]

    tid = str(payload.get("target_id")).strip()
    slot_name = str(payload.get("slot_name")).strip()
    key = _slot_key(tid, slot_name)

    if key in overrides:
        del overrides[key]

    decor["material_overrides"] = overrides
    setattr(snapshot, "decor_state", decor)
    return {"ok": True, "override_key": key}

# --- Pivot / Origin Editing helpers ---
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
    objs: List[Dict[str, Any]] = body["objects"]

    object_id = str(payload.get("object_id"))
    obj = _find_object(objs, object_id)
    if not obj:
        return {"ok": False, "error": "object not found"}

    pivot = payload.get("pivot") or {}
    obj["pivot"] = {
        "x": _num(pivot.get("x", 0)),
        "y": _num(pivot.get("y", 0)),
        "z": _num(pivot.get("z", 0)),
    }
    obj["version"] = int(obj.get("version") or 1)

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
    objs: List[Dict[str, Any]] = body["objects"]

    object_id = str(payload.get("object_id"))
    obj = _find_object(objs, object_id)
    if not obj:
        return {"ok": False, "error": "object not found"}

    obj["pivot"] = None
    obj["version"] = int(obj.get("version") or 1)

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
    objs: List[Dict[str, Any]] = body["objects"]

    object_id = str(payload.get("object_id"))
    preset = str(payload.get("preset"))
    obj = _find_object(objs, object_id)
    if not obj:
        return {"ok": False, "error": "object not found"}

    pivot = payload.get("pivot") or {}
    obj["pivot"] = {
        "x": _num(pivot.get("x", 0)),
        "y": _num(pivot.get("y", 0)),
        "z": _num(pivot.get("z", 0)),
    }
    obj["version"] = int(obj.get("version") or 1)

    body["objects"] = _sorted_objects(objs)
    setattr(snapshot, "body_state", body)
    return {
        "ok": True,
        "object_id": object_id,
        "preset": preset,
        "pivot": obj["pivot"],
    }
