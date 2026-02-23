from __future__ import annotations

from typing import Dict, Any

from app.services.transform_with_snapping import normalize_transform_payload_with_snapping
from app.services.axis_locks import apply_axis_lock_to_payload


def normalize_transform_payload(*, payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    Tier 7.3 + 7.4 combined normalizer.
    snapping first, then axis locks.
    """
    p = normalize_transform_payload_with_snapping(payload=payload)
    p = apply_axis_lock_to_payload(payload=p)
    return p
