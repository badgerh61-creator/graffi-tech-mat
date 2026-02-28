from __future__ import annotations
from typing import Any, Dict, List, Optional
import uuid

ALLOWED_BLEND = {"normal", "multiply", "add"}

def _ensure_decor(snapshot) -> Dict[str, Any]:
    decor = getattr(snapshot, "decor_state", None) or {}
    if not isinstance(decor, dict):
        decor = {}
    if "decals" not in decor or not isinstance(decor.get("decals"), list):
        decor["decals"] = []
    return decor

def _find_index(decals: List[Dict[str, Any]], decal_id: str) -> int:
    for i, d in enumerate(decals):
        if isinstance(d, dict) and str(d.get("id")) == str(decal_id):
            return i
    return -1

def _clamp01(x: float) -> float:
    if x < 0: return 0.0
    if x > 1: return 1.0
    return float(x)

def validate_create(payload: Dict[str, Any]) -> Optional[str]:
    if not str(payload.get("target_id") or "").strip():
        return "target_id required"
    if not str(payload.get("asset_ref") or "").strip():
        return "asset_ref required"
    initial = payload.get("initial") or {}
    op = float(initial.get("opacity", 1.0))
    if op < 0 or op > 1:
        return "opacity must be within [0..1]"
    blend = str(initial.get("blend", "normal"))
    if blend not in ALLOWED_BLEND:
        return "blend invalid"
    return None

def validate_update(payload: Dict[str, Any]) -> Optional[str]:
    if not str(payload.get("decal_id") or "").strip():
        return "decal_id required"
    patch = payload.get("patch")
    if not isinstance(patch, dict):
        return "patch must be an object"
    if "opacity" in patch:
        op = float(patch.get("opacity"))
        if op < 0 or op > 1:
            return "opacity must be within [0..1]"
    if "blend" in patch:
        blend = str(patch.get("blend"))
        if blend not in ALLOWED_BLEND:
            return "blend invalid"
    if "id" in patch:
        return "id cannot be patched"
    return None

def validate_delete(payload: Dict[str, Any]) -> Optional[str]:
    if not str(payload.get("decal_id") or "").strip():
        return "decal_id required"
    return None

def apply_create(snapshot, payload: Dict[str, Any]) -> Dict[str, Any]:
    decor = _ensure_decor(snapshot)
    decals: List[Dict[str, Any]] = decor["decals"]

    initial = payload.get("initial") or {}

    decal_id = f"dec-{uuid.uuid4().hex[:12]}"
    decal = {
        "id": decal_id,
        "enabled": True,
        "target_id": payload.get("target_id"),
        "asset_ref": payload.get("asset_ref"),
        "position": initial.get("position") or {"x": 0, "y": 0, "z": 0},
        "rotation_euler": initial.get("rotation_euler") or {"x": 0, "y": 0, "z": 0},
        "scale": initial.get("scale") or {"x": 1, "y": 1, "z": 1},
        "opacity": _clamp01(float(initial.get("opacity", 1.0))),
        "blend": str(initial.get("blend", "normal")),
        "z_offset": float(initial.get("z_offset", 0.001)),
        "meta": initial.get("meta") or {},
    }

    decals.append(decal)
    decor["decals"] = decals
    setattr(snapshot, "decor_state", decor)
    return {"ok": True, "decal_id": decal_id}

def apply_update(snapshot, payload: Dict[str, Any]) -> Dict[str, Any]:
    decor = _ensure_decor(snapshot)
    decals: List[Dict[str, Any]] = decor["decals"]

    decal_id = str(payload.get("decal_id"))
    idx = _find_index(decals, decal_id)
    if idx < 0:
        return {"ok": False, "error": "decal not found"}

    patch = payload.get("patch") or {}
    d = decals[idx]

    # safe patch
    for k, v in patch.items():
        if k == "id":
            continue
        if k == "opacity":
            d[k] = _clamp01(float(v))
        else:
            d[k] = v

    decals[idx] = d
    decor["decals"] = decals
    setattr(snapshot, "decor_state", decor)
    return {"ok": True, "decal_id": decal_id}

def apply_delete(snapshot, payload: Dict[str, Any]) -> Dict[str, Any]:
    decor = _ensure_decor(snapshot)
    decals: List[Dict[str, Any]] = decor["decals"]

    decal_id = str(payload.get("decal_id"))
    idx = _find_index(decals, decal_id)
    if idx < 0:
        return {"ok": False, "error": "decal not found"}

    decals.pop(idx)
    decor["decals"] = decals
    setattr(snapshot, "decor_state", decor)
    return {"ok": True, "decal_id": decal_id}
