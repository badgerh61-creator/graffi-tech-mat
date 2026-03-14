from __future__ import annotations
from typing import Dict, Any, List

PAINT_LIBRARY: Dict[str, Dict[str, Any]] = {
    "paint_gloss_red": {
        "name": "Gloss Red",
        "finish": "gloss",
        "color": "#D00000",
        "roughness": 0.20,
        "metalness": 0.10,
        "opacity": 1.0,
    },
    "paint_gloss_black": {
        "name": "Gloss Black",
        "finish": "gloss",
        "color": "#111111",
        "roughness": 0.18,
        "metalness": 0.12,
        "opacity": 1.0,
    },
    "paint_matte_black": {
        "name": "Matte Black",
        "finish": "matte",
        "color": "#141414",
        "roughness": 0.90,
        "metalness": 0.00,
        "opacity": 1.0,
    },
    "paint_satin_silver": {
        "name": "Satin Silver",
        "finish": "satin",
        "color": "#A8A8A8",
        "roughness": 0.45,
        "metalness": 0.30,
        "opacity": 1.0,
    },
    "paint_metallic_blue": {
        "name": "Metallic Blue",
        "finish": "metallic",
        "color": "#1F4BA8",
        "roughness": 0.28,
        "metalness": 0.75,
        "opacity": 1.0,
    },
    "paint_chrome_like": {
        "name": "Chrome-like",
        "finish": "chrome_like",
        "color": "#D8D8D8",
        "roughness": 0.12,
        "metalness": 1.00,
        "opacity": 1.0,
    },
}

def list_paint_library() -> List[Dict[str, Any]]:
    return [{"id": k, **PAINT_LIBRARY[k]} for k in sorted(PAINT_LIBRARY.keys())]

def is_valid_paint_preset(preset_id: str) -> bool:
    return str(preset_id) in PAINT_LIBRARY

def get_paint_preset(preset_id: str) -> Dict[str, Any]:
    return PAINT_LIBRARY[str(preset_id)]
