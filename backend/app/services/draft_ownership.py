# backend/app/services/draft_ownership.py

"""
Phase U kernel facade for draft ownership & locking.
Stable imports for kernel stress tests.
"""

from app.services.snapshot_drafts import (
    acquire_draft_lock,
    release_draft_lock,
    require_draft_owner,
)
from app.services.ownership_handoff import (
    handoff_draft_ownership,
)


def is_draft_owner(*, snapshot, user, db=None) -> bool:
    """
    Predicate form of draft ownership check.
    db is accepted for kernel compatibility only.
    """
    return getattr(snapshot, "owner_user_id", None) == user.id


__all__ = [
    "acquire_draft_lock",
    "release_draft_lock",
    "require_draft_owner",
    "is_draft_owner",
    "handoff_draft_ownership",
]

