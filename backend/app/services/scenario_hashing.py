from __future__ import annotations

import hashlib
import json
from typing import Any, Dict


def stable_hash(obj: Any) -> str:
    raw = json.dumps(obj, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


def compute_scenario_hash(
    *,
    scenario: Dict[str, Any],
    template_key: str | None,
    template_version: str | None,
    engine_version: str,
) -> str:
    payload = {
        "scenario": scenario,
        "template_key": template_key or "",
        "template_version": template_version or "",
        "engine_version": engine_version,
    }
    return stable_hash(payload)
