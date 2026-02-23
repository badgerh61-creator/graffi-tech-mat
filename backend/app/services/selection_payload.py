from __future__ import annotations

from typing import Any, Dict
from fastapi import HTTPException

PIVOT_MODES = {"bbox_center", "world_origin", "custom"}


def _is_num(v: Any) -> bool:
    return isinstance(v, (int, float)) and v == v  # not NaN


def normalize_multiselect_payload(*, payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    Pure validator/normalizer for Tier 7.5.
    Returns a NEW dict; never mutates input.
    """
    p = dict(payload or {})

    ids = p.get("selected_target_ids")
    if ids is None:
        # single-target transforms remain valid
        return p

    if not isinstance(ids, list) or len(ids) == 0 or not all(isinstance(x, str) and x for x in ids):
        raise HTTPException(422, "selected_target_ids must be a non-empty list of strings")

    pivot_mode = p.get("pivot_mode") or "bbox_center"
    if not isinstance(pivot_mode, str) or pivot_mode not in PIVOT_MODES:
        raise HTTPException(422, "invalid pivot_mode")
    p["pivot_mode"] = pivot_mode

    if pivot_mode == "custom":
        pivot = p.get("pivot")
        if not isinstance(pivot, dict):
            raise HTTPException(422, "pivot required when pivot_mode=custom")
        for k in ("x", "y", "z"):
            if k not in pivot or not _is_num(pivot[k]):
                raise HTTPException(422, "pivot must include numeric x,y,z")
        p["pivot"] = {"x": float(pivot["x"]), "y": float(pivot["y"]), "z": float(pivot["z"])}

    bbox = p.get("selection_bbox")
    if bbox is not None:
        if not isinstance(bbox, dict) or "min" not in bbox or "max" not in bbox:
            raise HTTPException(422, "selection_bbox must include min/max")
        for corner in ("min", "max"):
            c = bbox[corner]
            if not isinstance(c, dict):
                raise HTTPException(422, "selection_bbox corners must be objects")
            for k in ("x", "y", "z"):
                if k not in c or not _is_num(c[k]):
                    raise HTTPException(422, "selection_bbox corners must include numeric x,y,z")
        p["selection_bbox"] = {
            "min": {k: float(bbox["min"][k]) for k in ("x", "y", "z")},
            "max": {k: float(bbox["max"][k]) for k in ("x", "y", "z")},
        }

    return p
