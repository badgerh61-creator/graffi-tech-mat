from app.kernel import acquire_draft_lock, release_draft_lock, handoff_draft_ownership
from app.services.presence_sessions import start_session

# backend/tests/phase_t_u/conftest.py
# Phase T–U Kernel Injection Layer (AUTHORITATIVE, REQUIRED)

import pytest
import builtins
from datetime import timedelta

from app.models.conflict import SnapshotConflict

# Canonical kernel imports
from app.kernel.t_authority import require_draft_authority
from app.kernel.execute_tool import execute_tool
from app.kernel import handoff_draft_ownership

from app.services.audit import get_audit_events
from app.services.presence_sessions import start_session
from app.services.presence_service import mark_user_present
from app.services.draft_lock_service import (
    acquire_draft_lock,
    release_draft_lock,
)

# ─────────────────────────────────────────────
# USER FIXTURES (REQUIRED BY PHASE T–U TESTS)
# ─────────────────────────────────────────────

@pytest.fixture
def target_user(editor_user):
    # Secondary editor used for handoff tests
    return editor_user


@pytest.fixture
def non_owner_user(viewer_user):
    # Viewer used to assert ownership violations
    return viewer_user


# ─────────────────────────────────────────────
# SNAPSHOT FIXTURES
# ─────────────────────────────────────────────

@pytest.fixture
def conflicted_draft_snapshot(db, draft_snapshot):
    conflict = SnapshotConflict(
        snapshot_id=draft_snapshot.id,
        reason="Concurrent modification detected",
    )
    db.add(conflict)
    db.commit()
    return draft_snapshot


# ─────────────────────────────────────────────
# TIME CONTROL (TEST-ONLY)
# ─────────────────────────────────────────────

def _advance_time(seconds: int):
    from app.models.presence_session import PresenceSession
    from app.db.session import SessionLocal

    db = SessionLocal()
    for session in db.query(PresenceSession).all():
        session.expires_at -= timedelta(seconds=seconds)
    db.commit()
    db.close()


# ─────────────────────────────────────────────
# 🔥 KERNEL SYMBOL INJECTION (SINGLE SOURCE OF TRUTH)
# ─────────────────────────────────────────────

@pytest.fixture(autouse=True)
def inject_kernel_symbols(monkeypatch):
    # Authority & execution
    monkeypatch.setattr(builtins, "require_draft_authority", require_draft_authority, raising=False)
    monkeypatch.setattr(builtins, "execute_tool", execute_tool, raising=False)

    # Draft ownership
    monkeypatch.setattr(builtins, "acquire_draft_lock", acquire_draft_lock, raising=False)
    monkeypatch.setattr(builtins, "release_draft_lock", release_draft_lock, raising=False)
    monkeypatch.setattr(builtins, "handoff_draft_ownership", handoff_draft_ownership, raising=False)

    # Presence / sessions
    monkeypatch.setattr(builtins, "start_session", start_session, raising=False)
    monkeypatch.setattr(builtins, "mark_user_present", mark_user_present, raising=False)
    monkeypatch.setattr(builtins, "advance_time", _advance_time, raising=False)

    # Audit
    monkeypatch.setattr(builtins, "get_audit_events", get_audit_events, raising=False)

