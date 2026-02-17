from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Optional

from app.studio.kernel_errors import KernelRejection
from app.studio.structural_guards import (
    require_tool_exists,
    require_station_exists,
    require_station_tool_flow,
    require_snapshot_allows,
    require_user_capability,
    require_mode,
)


@dataclass(frozen=True)
class KernelDecision:
    allowed: bool
    reason: Optional[str] = None
    mode: Optional[str] = None
    tool: Optional[str] = None
    payload: Optional[Dict[str, Any]] = None


def evaluate_tool_invocation(
    *,
    user,
    snapshot,
    station: str,
    tool: str,
    payload: Dict[str, Any],
) -> KernelDecision:
    """
    Tier 4.5 — READ-ONLY kernel evaluation.

    Uses Phase T structural guards exactly as authored.
    NO DB writes.
    NO snapshot mutation.
    """
    try:
        require_user_capability(user)
        require_station_exists(station)
        require_tool_exists(tool)
        require_station_tool_flow(station, tool)
        require_snapshot_allows(snapshot, tool)

        mode = require_mode(
            snapshot=snapshot,
            user=user,
            station=station,
            tool=tool,
        )

        return KernelDecision(
            allowed=True,
            reason=None,
            mode=getattr(mode, "value", str(mode)),
            tool=tool,
            payload=payload,
        )

    except KernelRejection as kr:
        return KernelDecision(
            allowed=False,
            reason=getattr(kr, "reason", "unknown"),
            mode=None,
            tool=tool,
            payload=payload,
        )

