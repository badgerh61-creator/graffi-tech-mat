from __future__ import annotations
from typing import Dict, Any, List

# Tier 7.42 minimal preset list
PRESETS: Dict[str, Dict[str, Any]] = {
    "paint_gloss_red": {"kind": "standard", "metalness": 0.1, "roughness": 0.2, "color": "#d00000"},
    "matte_black": {"kind": "standard", "metalness": 0.0, "roughness": 0.9, "color": "#111111"},
    "chrome": {"kind": "standard", "metalness": 1.0, "roughness": 0.2, "color": "#dddddd"},
    "plastic_gray": {"kind": "standard", "metalness": 0.0, "roughness": 0.6, "color": "#777777"},
}

def list_presets() -> List[Dict[str, Any]]:
    # stable order
    return [{"id": k, **PRESETS[k]} for k in sorted(PRESETS.keys())]

def is_valid_preset(preset_id: str) -> bool:
    return str(preset_id) in PRESETS
