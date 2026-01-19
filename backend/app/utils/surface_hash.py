import hashlib
import json
from typing import Any, Iterable


def _curve_identity(curve: Any, index: int) -> str:
    """
    Return a deterministic identity for a curve.

    Priority:
    1. Explicit object attribute `id`
    2. Dict-based `id`
    3. Positional fallback (index-based, deterministic)

    This intentionally avoids repr(), memory addresses,
    or object hashes, which are non-deterministic.
    """

    # Object-style curve with explicit ID
    if hasattr(curve, "id"):
        return str(curve.id)

    # Dict-style curve with ID
    if isinstance(curve, dict) and "id" in curve:
        return str(curve["id"])

    # Deterministic fallback: positional identity
    return f"curve_index_{index}"


def compute_surface_hash(
    *,
    curves: Iterable[Any],
    params: dict | None,
    method: str,
) -> str:
    """
    Compute a deterministic hash for a derived surface.

    Determinism guarantees:
    - Same curves (order matters)
    - Same params
    - Same method
    => Same hash

    No geometry, meshes, or memory addresses are involved.
    """

    payload = {
        "curves": [
            _curve_identity(curve, index)
            for index, curve in enumerate(curves)
        ],
        "params": params or {},
        "method": method,
    }

    # Canonical JSON serialization
    raw = json.dumps(payload, sort_keys=True).encode("utf-8")

    return hashlib.sha256(raw).hexdigest()

