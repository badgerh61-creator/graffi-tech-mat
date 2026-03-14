from __future__ import annotations
from typing import Any, Dict, List, Optional
import copy
import uuid

def _ensure_state(snapshot):
    body = getattr(snapshot, "body_state", None) or {}
    if not isinstance(body, dict):
        body = {}

    decor = getattr(snapshot, "decor_state", None) or {}
    if not isinstance(decor, dict):
        decor = {}

    if "objects" not in body or not isinstance(body.get("objects"), list):
        body["objects"] = []

    if "material_overrides" not in decor or not isinstance(decor.get("material_overrides"), dict):
        decor["material_overrides"] = {}

    if "decals" not in decor or not isinstance(decor.get("decals"), list):
        decor["decals"] = []

    if "variant_sets" not in decor or not isinstance(decor.get("variant_sets"), list):
        decor["variant_sets"] = []

    return body, decor

def _sorted_variants(variants: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    return sorted(variants, key=lambda v: str(v.get("id")))

def _find_variant(variants: List[Dict[str, Any]], variant_id: str) -> Optional[Dict[str, Any]]:
    for v in variants:
        if isinstance(v, dict) and str(v.get("id")) == str(variant_id):
            return v
    return None

def validate_save_variant(payload: Dict[str, Any]) -> Optional[str]:
    name = str(payload.get("name") or "").strip()
    if not name:
        return "name required"
    return None

def apply_save_variant(snapshot, payload: Dict[str, Any]) -> Dict[str, Any]:
    body, decor = _ensure_state(snapshot)

    objects = body["objects"]
    material_overrides = decor["material_overrides"]
    decals = decor["decals"]
    variants = decor["variant_sets"]

    object_enabled = {
        str(obj.get("id")): bool(obj.get("enabled", True))
        for obj in objects
        if isinstance(obj, dict) and obj.get("id") is not None
    }

    variant = {
        "id": f"var-{uuid.uuid4().hex[:12]}",
        "name": str(payload.get("name")).strip(),
        "payload": {
            "material_overrides": copy.deepcopy(material_overrides),
            "decals": copy.deepcopy(decals),
            "object_enabled": copy.deepcopy(object_enabled),
        },
        "version": 1,
    }

    variants.append(variant)
    decor["variant_sets"] = _sorted_variants(variants)
    setattr(snapshot, "decor_state", decor)
    return {"ok": True, "variant_id": variant["id"]}

def validate_apply_variant(payload: Dict[str, Any]) -> Optional[str]:
    variant_id = str(payload.get("variant_id") or "").strip()
    if not variant_id:
        return "variant_id required"
    return None

def apply_apply_variant(snapshot, payload: Dict[str, Any]) -> Dict[str, Any]:
    body, decor = _ensure_state(snapshot)

    variants = decor["variant_sets"]
    variant_id = str(payload.get("variant_id"))
    variant = _find_variant(variants, variant_id)
    if not variant:
        return {"ok": False, "error": "variant not found"}

    vp = variant.get("payload") or {}

    decor["material_overrides"] = copy.deepcopy(vp.get("material_overrides") or {})
    decor["decals"] = copy.deepcopy(vp.get("decals") or [])

    enabled_map = vp.get("object_enabled") or {}
    for obj in body["objects"]:
        if not isinstance(obj, dict):
            continue
        oid = str(obj.get("id"))
        if oid in enabled_map:
            obj["enabled"] = bool(enabled_map[oid])

    setattr(snapshot, "body_state", body)
    setattr(snapshot, "decor_state", decor)

    return {"ok": True, "variant_id": variant_id}

def validate_delete_variant(payload: Dict[str, Any]) -> Optional[str]:
    variant_id = str(payload.get("variant_id") or "").strip()
    if not variant_id:
        return "variant_id required"
    return None

def apply_delete_variant(snapshot, payload: Dict[str, Any]) -> Dict[str, Any]:
    _, decor = _ensure_state(snapshot)
    variants = decor["variant_sets"]

    variant_id = str(payload.get("variant_id"))
    before = len(variants)
    variants = [v for v in variants if str(v.get("id")) != variant_id]

    decor["variant_sets"] = _sorted_variants(variants)
    setattr(snapshot, "decor_state", decor)

    return {"ok": True, "removed": before - len(variants), "variant_id": variant_id}
