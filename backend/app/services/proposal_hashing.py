from __future__ import annotations

import hashlib
import json
from typing import Any, Dict


def _canonical_dumps(obj: Any) -> str:
    """
    Deterministic JSON encoding:
    - sorted keys
    - no whitespace
    - stable separators
    """
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def compute_payload_hash(*, snapshot_id: int, tool: str, payload: Dict[str, Any]) -> str:
    base = {
        "snapshot_id": int(snapshot_id),
        "tool": str(tool),
        "payload": payload or {},
    }
    raw = _canonical_dumps(base).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()

