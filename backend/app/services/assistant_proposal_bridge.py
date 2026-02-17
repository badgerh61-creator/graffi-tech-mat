from __future__ import annotations

from typing import Any, Dict

from fastapi import HTTPException


def proposal_to_tool_request(*, proposal: Dict[str, Any]) -> Dict[str, Any]:
    """
    Tier 4.5 — Normalize assistant proposal → kernel tool request.

    Accepted keys:
      - tool: canonical tool name (e.g. "transform", "finalize")
      - station: station name (e.g. "geometry", "review")
      - payload: dict params (optional)

    This is validation + shaping only.
    """
    tool = proposal.get("tool") or proposal.get("tool_name") or proposal.get("action")
    station = proposal.get("station")
    payload = proposal.get("payload") or proposal.get("params") or {}

    if not tool or not isinstance(tool, str):
        raise HTTPException(422, "proposal missing tool")

    if not station or not isinstance(station, str):
        raise HTTPException(422, "proposal missing station")

    if not isinstance(payload, dict):
        raise HTTPException(422, "proposal payload must be an object")

    return {"tool": tool, "station": station, "payload": payload}

