from __future__ import annotations

from typing import Any, Dict


def assert_immutable_rejected(resp, expected_status: int = 409):
    assert resp.status_code == expected_status


def assert_forbidden(resp, expected_status: int = 403):
    assert resp.status_code == expected_status


def assert_ok(resp):
    assert resp.status_code == 200


def approx_equal(a: float, b: float, tol: float = 1e-6) -> bool:
    return abs(float(a) - float(b)) <= tol


def require_keys(d: Dict[str, Any], keys: list[str]):
    for k in keys:
        assert k in d, f"missing key: {k}"


# -----------------------------------------
# Phase V DB helpers (no endpoint required)
# -----------------------------------------

def force_db_lock(db, snapshot, user_id: int):
    """
    Simulate Phase U.2 lock in DB when lock endpoints are not mounted.
    Matches draft_lock_service expectations:
      - owner_user_id set
      - locked_at set
    """
    from datetime import datetime

    snapshot.owner_user_id = user_id
    snapshot.locked_at = datetime.utcnow()
    db.add(snapshot)
    db.commit()
    db.refresh(snapshot)
    return snapshot


def force_presence_session(
    db,
    *,
    user=None,
    user_id: int | None = None,
    snapshot=None,
    project_id: int | None = None,
    snapshot_id: int | None = None,   # accepted for compatibility; PresenceSession doesn't store it
    ttl_seconds: int = 3600,
):
    """
    Create an active PresenceSession row so require_active_session() passes.

    Supports any of these calling styles:
      - force_presence_session(db, user=<User>, snapshot=<RenderedSnapshot>)
      - force_presence_session(db, user_id=1, snapshot=<RenderedSnapshot>)
      - force_presence_session(db, user=<User>, project_id=123)
      - force_presence_session(db, user_id=1, project_id=123)
      - force_active_session(..., project_id=..., snapshot_id=...)  (snapshot_id ignored safely)

    IMPORTANT:
      - PresenceSession model does NOT have snapshot_id, so we accept it but ignore it.
    """
    from datetime import datetime, timedelta
    from app.models.presence_session import PresenceSession

    if user is None and user_id is None:
        raise TypeError("force_presence_session requires user or user_id")

    resolved_user_id = user_id if user_id is not None else getattr(user, "id", None)
    if resolved_user_id is None:
        raise TypeError("Could not resolve user.id")

    resolved_project_id = project_id
    if resolved_project_id is None and snapshot is not None:
        resolved_project_id = getattr(snapshot, "project_id", None)

    if resolved_project_id is None:
        raise TypeError("force_presence_session requires project_id or snapshot with project_id")

    now = datetime.utcnow()
    expires_at = now + timedelta(seconds=ttl_seconds)

    # Only set fields that exist on the model
    kwargs = {}
    if hasattr(PresenceSession, "user_id"):
        kwargs["user_id"] = resolved_user_id
    if hasattr(PresenceSession, "project_id"):
        kwargs["project_id"] = resolved_project_id
    if hasattr(PresenceSession, "created_at"):
        kwargs["created_at"] = now
    if hasattr(PresenceSession, "expires_at"):
        kwargs["expires_at"] = expires_at

    sess = PresenceSession(**kwargs)
    db.add(sess)
    db.commit()
    db.refresh(sess)
    return sess


# -----------------------------------------------------------------------------
# Compatibility alias (Phase V tests import this name)
# -----------------------------------------------------------------------------
def force_active_session(
    db,
    *,
    user=None,
    user_id: int | None = None,
    snapshot=None,
    project_id: int | None = None,
    snapshot_id: int | None = None,   # accepted; ignored
    ttl_seconds: int = 3600,
):
    """
    Backwards-compat alias used by Phase V tests.

    Some tests call:
      force_active_session(user_id=..., project_id=..., snapshot_id=...)

    We accept that signature and route to force_presence_session.
    """
    return force_presence_session(
        db,
        user=user,
        user_id=user_id,
        snapshot=snapshot,
        project_id=project_id,
        snapshot_id=snapshot_id,
        ttl_seconds=ttl_seconds,
    )


# -----------------------------------------
# Test auth override helper (dependency override)
# -----------------------------------------

def set_current_user(client, user):
    """
    Phase V tests sometimes want to force the current user without relying on headers.

    This uses FastAPI dependency_overrides so routes that depend on get_current_user
    will receive `user`.
    """
    from app.api.deps import get_current_user
    client.app.dependency_overrides[get_current_user] = lambda: user


def clear_current_user(client):
    """Remove the override set by set_current_user()."""
    from app.api.deps import get_current_user

    if get_current_user in client.app.dependency_overrides:
        del client.app.dependency_overrides[get_current_user]

