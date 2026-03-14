from __future__ import annotations
from typing import Dict, Any

def default_model_transform(kind: str) -> Dict[str, Any]:
    k = str(kind or "").lower()

    if k == "vehicle":
        return {
            "pos": {"x": 0, "y": 0, "z": 0},
            "rot": {"x": 0, "y": 0, "z": 0},
            "scale": {"x": 1, "y": 1, "z": 1},
        }

    if k == "wheel":
        return {
            "pos": {"x": 0, "y": 0, "z": 0},
            "rot": {"x": 0, "y": 0, "z": 0},
            "scale": {"x": 1, "y": 1, "z": 1},
        }

    return {
        "pos": {"x": 0, "y": 0, "z": 0},
        "rot": {"x": 0, "y": 0, "z": 0},
        "scale": {"x": 1, "y": 1, "z": 1},
    }
