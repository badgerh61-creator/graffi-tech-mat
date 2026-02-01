# backend/app/kernel/__init__.py
# Phase T / U — Canonical Kernel Surface (AUTHORITATIVE)

# Phase U.1 — Sessions
from app.services.presence_sessions import start_session, require_active_session

# Phase U.2 — Draft ownership
from app.services.draft_lock_service import (
    acquire_draft_lock,
    release_draft_lock,
)

# Phase U.4 — Ownership handoff
from app.services.draft_handoff_service import handoff_draft_ownership

# Phase T — Authority gate
from .t_authority import require_draft_authority

__all__ = [
    "start_session",
    "require_active_session",
    "acquire_draft_lock",
    "release_draft_lock",
    "handoff_draft_ownership",
    "require_draft_authority",
]

