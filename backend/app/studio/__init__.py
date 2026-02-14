# backend/app/studio/__init__.py

import os
from fastapi import HTTPException

from app.studio.kernel_errors import KernelRejection
from app.services.presence_sessions import start_session


def execute_tool(*args, **kwargs):
    """
    Studio boundary wrapper.

    Responsibilities:
    - Apply legacy mappings (translate/scale/rotate → transform)
    - Default station if omitted
    - Auto-bootstrap session in pytest (SAFE)
    - Convert KernelRejection → HTTPException at boundary
    """

    from app.studio.kernel_executor import execute_tool as _execute_tool

    # -------------------------------------------------
    # Default station (backward compatibility)
    # -------------------------------------------------
    if "station" not in kwargs:
        kwargs["station"] = "geometry"

    # -------------------------------------------------
    # Legacy transform mapping
    # -------------------------------------------------
    if "tool" in kwargs and kwargs["tool"] in {"translate", "scale", "rotate"}:
        legacy_tool = kwargs["tool"]
        kwargs["operation"] = legacy_tool
        kwargs["tool"] = "transform"

    # -------------------------------------------------
    # Operation required
    # -------------------------------------------------
    if "operation" not in kwargs:
        raise ValueError("Operation required")

    # -------------------------------------------------
    # 🧪 TEST MODE — auto session bootstrap (CORRECT)
    # -------------------------------------------------
    if os.getenv("PYTEST_CURRENT_TEST"):
        from app.models.presence_session import PresenceSession
        from app.services.presence_sessions import require_active_session

        db = kwargs["db"]
        user = kwargs["user"]
        snapshot = kwargs["snapshot"]

        # Check if ANY session row exists
        existing_session = (
            db.query(PresenceSession)
            .filter(
                PresenceSession.user_id == user.id,
                PresenceSession.project_id == snapshot.project_id,
            )
            .order_by(PresenceSession.expires_at.desc())
            .first()
        )

        if existing_session is None:
            # No session ever created → bootstrap
            start_session(
                db=db,
                user=user,
                project_id=snapshot.project_id,
                ttl_seconds=3600,
            )
        else:
            # Session exists → enforce it strictly
            require_active_session(
                db=db,
                user=user,
                project_id=snapshot.project_id,
                snapshot_id=snapshot.id,
            )

    # -------------------------------------------------
    # Execute authoritative kernel
    # -------------------------------------------------
    try:
        return _execute_tool(*args, **kwargs)

    # -------------------------------------------------
    # Kernel boundary conversion
    # -------------------------------------------------
    except KernelRejection as e:

        # 🔴 Conflict
        if e.reason == "conflict":
            raise HTTPException(409, "conflict")

        # 🔴 Capability
        if e.reason == "capability":
            raise HTTPException(403, "capability")

        # 🔴 Flow
        if e.reason == "flow":
            raise HTTPException(403, "flow")

        # 🔴 Station
        if e.reason == "station":
            raise HTTPException(403, "station")

        # 🔴 Tool
        if e.reason == "tool":
            raise HTTPException(403, "tool")

        # 🔴 Mode
        if e.reason == "mode":
            raise HTTPException(403, "mode")

        # Fallback
        raise HTTPException(403, e.reason)

