"""
Phase E.1 — Studio State Guard (READ-ONLY)

Explains why an action would be blocked,
without mutating anything.
"""

from app.services.read_view_guard import reject_mutation_from_read_view


def get_blocked_execution_context(*, db, user, snapshot):
    """
    Return a dict describing why execution would be blocked,
    or None if execution would be allowed.

    MUST NOT mutate.
    MUST NOT raise.
    """

    if snapshot is None:
        return None

    # -------------------------------------------------
    # Phase T.4 — Mode enforcement (read-only)
    # -------------------------------------------------
    try:
        reject_mutation_from_read_view(
            db=db,
            snapshot=snapshot,
            user=user,
        )
    except Exception as e:
        return {
            "code": "mode.read_only",
            "reason": str(e),
        }

    # -------------------------------------------------
    # Phase U / E.1 — Draft ownership blocking
    # -------------------------------------------------
    if snapshot.is_draft:
        if snapshot.owner_user_id is not None and snapshot.owner_user_id != user.id:
            return {
                "code": "snapshot.locked",
                "reason": "snapshot_locked_by_other_user",
            }

    return None

