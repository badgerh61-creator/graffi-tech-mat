from __future__ import annotations
from typing import Any, Dict, Optional

from app.services.materials.presets import is_valid_preset
from app.services.materials.params import validate_patch, clamp01, normalize_color


def _ensure_decor(snapshot) -> Dict[str, Any]:
    decor = getattr(snapshot, "decor_state", None) or {}
    if not isinstance(decor, dict):
        decor = {}
    if "material_overrides" not in decor or not isinstance(decor.get("material_overrides"), dict):
        decor["material_overrides"] = {}
    return decor


def _slot_key(target_id: str, slot_name: str) -> str:
    return f"{str(target_id)}::slot:{str(slot_name)}"


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


def apply_set(snapshot, payload: Dict[str, Any]) -> Dict[str, Any]:
    decor = _ensure_decor(snapshot)
    overrides: Dict[str, Any] = decor["material_overrides"]

    tid = str(payload.get("target_id"))
    preset = str(payload.get("preset"))

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

    tid = str(payload.get("target_id"))
    if tid in overrides:
        del overrides[tid]

    decor["material_overrides"] = overrides
    setattr(snapshot, "decor_state", decor)
    return {"ok": True, "target_id": tid}


def apply_update_params(snapshot, payload: Dict[str, Any]) -> Dict[str, Any]:
    decor = _ensure_decor(snapshot)
    overrides: Dict[str, Any] = decor["material_overrides"]

    tid = str(payload.get("target_id"))
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

    tid = str(payload.get("target_id"))
    slot_name = str(payload.get("slot_name"))
    preset = str(payload.get("preset"))

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

    tid = str(payload.get("target_id"))
    slot_name = str(payload.get("slot_name"))
    key = _slot_key(tid, slot_name)

    if key in overrides:
        del overrides[key]

    decor["material_overrides"] = overrides
    setattr(snapshot, "decor_state", decor)
    return {"ok": True, "override_key": key}
