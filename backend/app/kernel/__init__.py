"""
Phase T/U — Kernel Public Compatibility Surface

⚠️ DO NOT ADD LOGIC HERE.
⚠️ DO NOT ADD GUARDS HERE.
⚠️ DO NOT ADD MUTATION HERE.

This module exists ONLY to preserve legacy imports:

    from app.kernel import execute_tool
    from app.kernel import acquire_draft_lock
    ...

All real authority lives in:

    app.studio.kernel_executor
"""

# -------------------------------
# Studio execution (REAL ENGINE)
# -------------------------------

from app.studio import execute_tool


# -------------------------------
# Sessions (Phase U.1)
# -------------------------------

from app.services.presence_sessions import (
    start_session,
    require_active_session,
)


# -------------------------------
# Draft ownership (Phase U.2)
# -------------------------------

from app.services.draft_lock_service import (
    acquire_draft_lock,
    release_draft_lock,
    get_draft_lock,
    require_draft_owner,
)

from app.services.draft_lock_service import require_draft_owner as require_draft_authority


# -------------------------------
# Ownership handoff (Phase U.4)
# -------------------------------

from app.services.draft_handoff_service import (
    handoff_draft_ownership,
)


__all__ = [
    "execute_tool",
    "start_session",
    "require_active_session",
    "acquire_draft_lock",
    "release_draft_lock",
    "get_draft_lock",
    "require_draft_owner",
    "handoff_draft_ownership",
    "require_draft_authority",
]

