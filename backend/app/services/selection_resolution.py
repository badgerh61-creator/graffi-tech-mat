from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Tuple
from fastapi import HTTPException

KIND_ORDER = {
    "panel": 1,
    "curve": 2,
    "edge": 3,
    "vertex": 4,
}


@dataclass(frozen=True)
class HitCandidate:
    target_id: str
    kind: str
    depth: float
    priority: int = 0


@dataclass(frozen=True)
class SelectionState:
    selected_target_ids: List[str]
    active_target_id: Optional[str]
    winner: Optional[str]


def _parse_candidates(raw: Any) -> List[HitCandidate]:
    if raw is None:
        return []
    if not isinstance(raw, list):
        raise HTTPException(422, "hit_candidates must be a list")
    out: List[HitCandidate] = []
    for c in raw:
        if not isinstance(c, dict):
            raise HTTPException(422, "hit_candidates entries must be objects")
        tid = c.get("target_id")
        kind = c.get("kind")
        depth = c.get("depth")
        pr = c.get("priority", 0)

        if not isinstance(tid, str) or not tid:
            raise HTTPException(422, "hit_candidates.target_id required")
        if kind not in KIND_ORDER:
            raise HTTPException(422, "invalid hit candidate kind")
        if not isinstance(depth, (int, float)):
            raise HTTPException(422, "hit_candidates.depth must be numeric")
        if not isinstance(pr, int):
            raise HTTPException(422, "hit_candidates.priority must be int")

        out.append(HitCandidate(target_id=tid, kind=kind, depth=float(depth), priority=pr))
    return out


def choose_winner(candidates: List[HitCandidate]) -> Optional[HitCandidate]:
    if not candidates:
        return None

    def key(c: HitCandidate) -> Tuple[int, int, float, str]:
        # priority desc -> kind desc -> depth asc -> id asc
        return (-c.priority, -KIND_ORDER[c.kind], c.depth, c.target_id)

    return sorted(candidates, key=key)[0]


def _normalize_ids(ids: Any) -> List[str]:
    if ids is None:
        return []
    if not isinstance(ids, list) or not all(isinstance(x, str) and x for x in ids):
        raise HTTPException(422, "selected_target_ids must be list[str]")
    return sorted(set(ids))


def resolve_selection(
    *,
    hit_candidates: Any,
    modifiers: Optional[Dict[str, Any]] = None,
    previous_selection: Optional[Dict[str, Any]] = None,
) -> SelectionState:
    """
    Deterministic selection resolution.
    Pure (no DB), returns stable ordering.
    """
    mods = dict(modifiers or {})
    shift = bool(mods.get("shift", False))
    ctrl = bool(mods.get("ctrl", False))

    prev = dict(previous_selection or {})
    selected = _normalize_ids(prev.get("selected_target_ids"))
    active = prev.get("active_target_id")
    if active is not None and not isinstance(active, str):
        raise HTTPException(422, "previous_selection.active_target_id must be string|null")
    if active and active not in selected:
        active = selected[0] if selected else None

    candidates = _parse_candidates(hit_candidates)
    winner = choose_winner(candidates)

    if winner is None:
        if shift or ctrl:
            return SelectionState(selected_target_ids=selected, active_target_id=active, winner=None)
        return SelectionState(selected_target_ids=[], active_target_id=None, winner=None)

    wid = winner.target_id

    if not shift and not ctrl:
        return SelectionState(selected_target_ids=[wid], active_target_id=wid, winner=wid)

    if shift:
        if wid in selected:
            selected = [x for x in selected if x != wid]
        else:
            selected = sorted(selected + [wid])
        active = (wid if wid in selected else (selected[0] if selected else None))
        return SelectionState(selected_target_ids=selected, active_target_id=active, winner=wid)

    # ctrl: add only
    if wid not in selected:
        selected = sorted(selected + [wid])
    active = wid
    return SelectionState(selected_target_ids=selected, active_target_id=active, winner=wid)
