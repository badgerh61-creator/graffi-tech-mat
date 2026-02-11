"""
Phase U.4 — Ownership Handoff Protocol

This module provides a named kernel primitive for transferring
draft ownership. It is intentionally minimal.
"""

from fastapi import HTTPException


def handoff_draft_ownership(*, db, snapshot, from_user, to_user):
    """
    Transfer draft ownership from one user to another.

    Kernel guarantees:
    - Snapshot must be draft
    - Caller must own the draft
    - Ownership transfer is atomic
    """

    if snapshot.status != "draft":
        raise HTTPException(409, "Snapshot is not a draft")

    # 🔒 Re-check after FOR UPDATE
    if snapshot.owner_user_id != from_user.id:
        raise HTTPException(403, "Caller does not own draft")

    # ✅ FIX — transfer ownership
    snapshot.owner_user_id = to_user.id

    db.add(snapshot)
    db.commit()
    db.refresh(snapshot)

    return snapshot

