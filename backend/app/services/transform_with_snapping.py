from __future__ import annotations

from typing import Any, Dict
from fastapi import HTTPException

from app.services.snapping import apply_snapping_to_transform_payload
from app.services.reference_frames_registry import is_known_frame


def normalize_transform_payload_with_snapping(*, payload: Dict[str, Any]) -> Dict[str, Any]:
    p = dict(payload or {})

    if p.get("snap"):
        frame_id = p.get("frame_id") or "world_xy"
        if not isinstance(frame_id, str):
            raise HTTPException(422, "frame_id must be a string")
        if not is_known_frame(frame_id):
            raise HTTPException(422, "unknown frame_id")
        p["frame_id"] = frame_id

    p = apply_snapping_to_transform_payload(payload=p)
    return p
