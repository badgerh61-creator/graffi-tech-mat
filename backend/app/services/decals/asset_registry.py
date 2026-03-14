from __future__ import annotations

import os
from typing import Any, Dict, List

"""
Tier 7.44 — Decal Asset Registry

Notes:
- Static, deterministic registry.
- asset_ref used by decals must match keys in ASSETS.
- URLs are derived deterministically from a base URL unless overridden.
- Legacy aliases (e.g. builtin://checker) are supported for backwards compatibility.
"""

DECAL_ASSET_BASE_URL = os.getenv(
    "DECAL_ASSET_BASE_URL",
    "http://127.0.0.1:8000/static/decals",
).rstrip("/")

# Stable asset IDs (treat as public API)
ASSETS: Dict[str, Dict[str, Any]] = {
    "asset-racing-stripe": {
        "name": "Racing Stripe",
        "path": "racing_stripe.png",
        "tags": ["stripe", "race"],
    },
    "asset-flame": {
        "name": "Flame",
        "path": "flame.png",
        "tags": ["flame", "hot"],
    },
    "asset-number-7": {
        "name": "Number 7",
        "path": "number_7.png",
        "tags": ["number"],
    },

    # --- Legacy compatibility asset ---
    # Used by older tests and legacy mutation flows
    "builtin://checker": {
        "name": "Checker",
        "path": "checker.png",
        "tags": ["checker", "pattern", "legacy"],
    },
}

# Optional alias table if more legacy refs appear later
ASSET_ALIASES: Dict[str, str] = {
    # example: "builtin://checkers": "builtin://checker"
}


def _resolve_alias(asset_ref: str) -> str:
    ref = str(asset_ref)
    return ASSET_ALIASES.get(ref, ref)


def resolve_asset_url(asset_ref: str) -> str:
    """
    Deterministic URL resolution.
    If an asset has explicit 'url', use it.
    Otherwise derive from base URL + path.
    """

    ref = _resolve_alias(asset_ref)

    if ref not in ASSETS:
        raise KeyError(f"Unknown decal asset_ref: {ref}")

    a = ASSETS[ref]

    if "url" in a and a["url"]:
        return str(a["url"])

    path = str(a.get("path") or "")
    return f"{DECAL_ASSET_BASE_URL}/{path.lstrip('/')}"


def list_decal_assets() -> List[Dict[str, Any]]:
    """
    Stable sorted output for deterministic UI rendering.
    """
    out: List[Dict[str, Any]] = []

    for k in sorted(ASSETS.keys()):
        a = ASSETS[k]
        out.append(
            {
                "id": k,
                "name": a.get("name"),
                "url": resolve_asset_url(k),
                "tags": a.get("tags") or [],
            }
        )

    return out


def is_valid_asset(asset_ref: str) -> bool:
    ref = _resolve_alias(asset_ref)
    return ref in ASSETS
