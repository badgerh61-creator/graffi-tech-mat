from __future__ import annotations
from typing import Any, Dict, List, Optional
import re
import uuid

from app.services.materials.paint_library import (
    is_valid_paint_preset,
    get_paint_preset,
)

HEX_RE = re.compile(r"^#[0-9A-Fa-f]{6}$")
VALID_FINISHES = {"gloss", "matte", "satin", "metallic", "chrome_like"}


# ------------------------------------------------------------
# helpers
# ------------------------------------------------------------

def _ensure_decor(snapshot) -> Dict[str, Any]:
    body = getattr(snapshot, "body_state", None) or {}

    decor = body.get("decor_state")
    if not isinstance(decor, dict):
        decor = {}

    if "material_overrides" not in decor:
        decor["material_overrides"] = {}

    if "paint_swatches" not in decor:
        decor["paint_swatches"] = []

    body["decor_state"] = decor
    snapshot.body_state = body

    setattr(snapshot, "decor_state", decor)

    return decor


# 🔥 FIXED — writes to body_state.scene.objects
def _ensure_material_state(snapshot, target_id: str, paint: Dict[str, Any]):
    """
    Tier 6G — write paint into scene objects
    """

    body = getattr(snapshot, "body_state", None) or {}
    scene = body.get("scene") or {}
    objects = scene.get("objects")

    if not isinstance(objects, list):
        return

    for obj in objects:
        if str(obj.get("id")) != str(target_id):
            continue

        if "material_state" not in obj:
            obj["material_state"] = {}

        obj["material_state"]["paint"] = {
            "color": paint.get("color"),
            "roughness": float(paint.get("roughness", 0.5)),
            "metalness": float(paint.get("metalness", 0.0)),
        }

    scene["objects"] = objects
    body["scene"] = scene
    snapshot.body_state = body


def _sorted_swatches(swatches: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    return sorted(swatches, key=lambda s: str(s.get("id")))


def _find_swatch(
    swatches: List[Dict[str, Any]], swatch_id: str
) -> Optional[Dict[str, Any]]:
    for s in swatches:
        if isinstance(s, dict) and str(s.get("id")) == str(swatch_id):
            return s
    return None


# ------------------------------------------------------------
# preset apply
# ------------------------------------------------------------

def validate_apply_library_preset(payload: Dict[str, Any]) -> Optional[str]:
    tid = str(payload.get("target_id") or "").strip()
    if not tid:
        return "target_id required"

    preset = str(
      payload.get("preset") or payload.get("preset_id") or ""
    ).strip()
    
    if not preset:
        return "preset required"

    if not is_valid_paint_preset(preset):
        return "preset invalid"

    return None


def apply_apply_library_preset(snapshot, payload: Dict[str, Any]) -> Dict[str, Any]:
    decor = _ensure_decor(snapshot)
    overrides: Dict[str, Any] = decor["material_overrides"]

    tid = str(payload.get("target_id"))
    preset_id = str(payload.get("preset") or payload.get("preset_id"))
    preset = get_paint_preset(preset_id)

    overrides[tid] = {
        "preset": preset_id,
        "params": {
            "color": preset["color"],
            "roughness": float(preset["roughness"]),
            "metalness": float(preset["metalness"]),
            "opacity": float(preset.get("opacity", 1.0)),
        },
        "version": 1,
    }

    decor["material_overrides"] = overrides
    setattr(snapshot, "decor_state", decor)

    _ensure_material_state(
        snapshot,
        tid,
        {
            "color": preset["color"],
            "roughness": preset["roughness"],
            "metalness": preset["metalness"],
        },
    )

    return {"ok": True, "target_id": tid, "preset": preset_id}


# ------------------------------------------------------------
# swatch save
# ------------------------------------------------------------

def validate_save_swatch(payload: Dict[str, Any]) -> Optional[str]:
    name = str(payload.get("name") or "").strip()
    if not name:
        return "name required"

    color = str(payload.get("color") or "").strip()
    if not HEX_RE.match(color):
        return "color must be #RRGGBB"

    finish = str(payload.get("finish") or "").strip()
    if finish not in VALID_FINISHES:
        return "finish invalid"

    return None


def apply_save_swatch(snapshot, payload: Dict[str, Any]) -> Dict[str, Any]:
    decor = _ensure_decor(snapshot)
    swatches: List[Dict[str, Any]] = decor["paint_swatches"]

    swatch = {
        "id": f"sw-{uuid.uuid4().hex[:12]}",
        "name": str(payload.get("name")),
        "color": str(payload.get("color")).upper(),
        "finish": str(payload.get("finish")),
        "version": 1,
    }

    swatches.append(swatch)

    decor["paint_swatches"] = _sorted_swatches(swatches)
    setattr(snapshot, "decor_state", decor)

    return {"ok": True, "swatch_id": swatch["id"]}


# ------------------------------------------------------------
# swatch delete
# ------------------------------------------------------------

def validate_delete_swatch(payload: Dict[str, Any]) -> Optional[str]:
    swatch_id = str(payload.get("swatch_id") or "").strip()
    if not swatch_id:
        return "swatch_id required"

    return None


def apply_delete_swatch(snapshot, payload: Dict[str, Any]) -> Dict[str, Any]:
    decor = _ensure_decor(snapshot)
    swatches: List[Dict[str, Any]] = decor["paint_swatches"]

    swatch_id = str(payload.get("swatch_id"))

    before = len(swatches)
    swatches = [s for s in swatches if str(s.get("id")) != swatch_id]

    decor["paint_swatches"] = _sorted_swatches(swatches)
    setattr(snapshot, "decor_state", decor)

    return {
        "ok": True,
        "removed": before - len(swatches),
        "swatch_id": swatch_id,
    }


# ------------------------------------------------------------
# swatch apply
# ------------------------------------------------------------

def validate_apply_swatch(payload: Dict[str, Any]) -> Optional[str]:
    tid = str(payload.get("target_id") or "").strip()
    if not tid:
        return "target_id required"

    swatch_id = str(payload.get("swatch_id") or "").strip()
    if not swatch_id:
        return "swatch_id required"

    return None


def _finish_defaults(finish: str) -> Dict[str, float]:
    if finish == "gloss":
        return {"roughness": 0.20, "metalness": 0.10, "opacity": 1.0}
    if finish == "matte":
        return {"roughness": 0.90, "metalness": 0.00, "opacity": 1.0}
    if finish == "satin":
        return {"roughness": 0.45, "metalness": 0.25, "opacity": 1.0}
    if finish == "metallic":
        return {"roughness": 0.28, "metalness": 0.75, "opacity": 1.0}
    if finish == "chrome_like":
        return {"roughness": 0.12, "metalness": 1.00, "opacity": 1.0}

    return {"roughness": 0.60, "metalness": 0.00, "opacity": 1.0}


def apply_apply_swatch(snapshot, payload: Dict[str, Any]) -> Dict[str, Any]:
    decor = _ensure_decor(snapshot)
    overrides: Dict[str, Any] = decor["material_overrides"]
    swatches: List[Dict[str, Any]] = decor["paint_swatches"]

    tid = str(payload.get("target_id"))
    swatch_id = str(payload.get("swatch_id"))

    swatch = _find_swatch(swatches, swatch_id)
    if not swatch:
        return {"ok": False, "error": "swatch not found"}

    defaults = _finish_defaults(str(swatch.get("finish")))

    overrides[tid] = {
        "preset": f"swatch:{swatch_id}",
        "params": {
            "color": str(swatch.get("color")).upper(),
            "roughness": defaults["roughness"],
            "metalness": defaults["metalness"],
            "opacity": defaults["opacity"],
        },
        "version": 1,
    }

    decor["material_overrides"] = overrides
    setattr(snapshot, "decor_state", decor)

    _ensure_material_state(
        snapshot,
        tid,
        {
            "color": str(swatch.get("color")).upper(),
            "roughness": defaults["roughness"],
            "metalness": defaults["metalness"],
        },
    )

    return {"ok": True, "target_id": tid, "swatch_id": swatch_id}
