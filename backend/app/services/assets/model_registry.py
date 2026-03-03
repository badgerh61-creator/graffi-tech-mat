from __future__ import annotations
from typing import Any, Dict, List

ASSETS: Dict[str, Dict[str, Any]] = {
    "asset-vehicle-demo": {
        "name": "Demo Vehicle",
        "url": "https://example.com/assets/models/demo_vehicle.glb",
        "kind": "vehicle",
        "tags": ["vehicle", "demo"],
    },
    "asset-cube-demo": {
        "name": "Cube Demo",
        "url": "https://example.com/assets/models/cube.glb",
        "kind": "prop",
        "tags": ["demo"],
    },
}

def list_model_assets() -> List[Dict[str, Any]]:
    return [{"id": k, **ASSETS[k]} for k in sorted(ASSETS.keys())]

def is_valid_model_asset(asset_id: str) -> bool:
    return str(asset_id) in ASSETS

def resolve_model_url(asset_id: str) -> str:
    return ASSETS[str(asset_id)]["url"]
