from __future__ import annotations
from typing import Any, Dict, Optional


def emit_metric(name: str, value: float | int = 1, tags: Optional[Dict[str, Any]] = None) -> None:
    """
    Ops-grade compatibility shim.

    Phase H.3 uses emit_metric() for observability, but in this repo
    we keep it as a no-op unless/until Phase P metrics sink exists.

    MUST NOT raise.
    MUST be safe in tests and production.
    """
    return

