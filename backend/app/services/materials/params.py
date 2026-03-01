from __future__ import annotations

from typing import Any, Dict, Optional
import re

HEX_RE = re.compile(r"^#[0-9a-fA-F]{6}$")
ALLOWED_KEYS = {"color", "roughness", "metalness", "opacity"}


def validate_patch(patch: Dict[str, Any]) -> Optional[str]:
    if not isinstance(patch, dict):
        return "patch must be an object"

    for k in patch.keys():
        if k not in ALLOWED_KEYS:
            return f"invalid key: {k}"

    if "color" in patch:
        c = str(patch.get("color") or "")
        if not HEX_RE.match(c):
            return "color must be #RRGGBB"

    for k in ("roughness", "metalness", "opacity"):
        if k in patch:
            v = patch.get(k)
            try:
                f = float(v)
            except Exception:
                return f"{k} must be a number"
            if not (f == f):  # NaN
                return f"{k} must be finite"
            # out-of-range is ok; apply clamps deterministically

    return None


def clamp01(x: float) -> float:
    if x < 0:
        return 0.0
    if x > 1:
        return 1.0
    return float(x)


def normalize_color(c: str) -> str:
    return str(c).upper()
