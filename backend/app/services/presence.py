# Canonical Phase U.1 exports (alias only)

from app.services.presence_sessions import (
    start_session,
    require_active_session,
)

from app.services.presence_service import (
    is_user_present,
    mark_user_present,
    mark_user_absent,
)

__all__ = [
    "start_session",
    "require_active_session",
    "is_user_present",
    "mark_user_present",
    "mark_user_absent",
]

