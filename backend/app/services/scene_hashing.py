import json
import hashlib
from typing import Any


def canonical_scene_hash(scene_state: dict) -> str:
    """
    Deterministically hash a scene state.
    - Order-independent
    - Stable across sessions
    - Excludes non-deterministic fields
    """

    # Ensure deterministic ordering
    normalized = json.dumps(
        scene_state,
        sort_keys=True,
        separators=(",", ":"),
    )

    return hashlib.sha256(normalized.encode("utf-8")).hexdigest()

