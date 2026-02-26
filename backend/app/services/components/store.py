from __future__ import annotations
from typing import Any, Dict, Optional, List

def get_components(snapshot) -> List[Dict[str, Any]]:
    body = snapshot.body_state or {}
    raw = body.get("components", [])
    return raw if isinstance(raw, list) else []

def find_component(snapshot, component_id: str) -> Optional[Dict[str, Any]]:
    for c in get_components(snapshot):
        if isinstance(c, dict) and str(c.get("id")) == str(component_id):
            return c
    return None

def upsert_component(snapshot, next_component: Dict[str, Any]) -> None:
    """
    Mutates snapshot.body_state in-memory (ONLY for apply path).
    Caller must be the governed mutation pipeline.
    """
    body = snapshot.body_state or {}
    comps = body.get("components", [])
    if not isinstance(comps, list):
        comps = []

    cid = str(next_component.get("id"))
    replaced = False
    for i, c in enumerate(comps):
        if isinstance(c, dict) and str(c.get("id")) == cid:
            comps[i] = next_component
            replaced = True
            break
    if not replaced:
        comps.append(next_component)

    body["components"] = comps
    snapshot.body_state = body
