# ============================================================
# Phase U.4 — Draft Ownership Handoff (TEST SUPPORT FIXTURES)
# ============================================================

import pytest

import app.services.presence_service as presence_service
from app.models.draft_lock import DraftLock
from app.services.draft_lock_service import acquire_draft_lock
from app.services.presence_service import mark_user_present


# ------------------------------------------------------------
# Ensure presence registry exists
# ------------------------------------------------------------
if not hasattr(presence_service, "_PRESENT_USER_IDS"):
    presence_service._PRESENT_USER_IDS = set()


# ------------------------------------------------------------
# CLEAR STATE *BEFORE* FIXTURES RUN
# ------------------------------------------------------------
@pytest.fixture(autouse=True)
def clear_runtime_state(db):
    """
    Phase U.4 tests assume:
    - no runtime draft locks
    - no users present
    """
    db.query(DraftLock).delete()
    db.commit()

    presence_service._PRESENT_USER_IDS.clear()


# ------------------------------------------------------------
# Target editor (handoff recipient, MUST be present)
# ------------------------------------------------------------
@pytest.fixture
def target_editor(editor_user):
    mark_user_present(editor_user)
    return editor_user


# ------------------------------------------------------------
# Offline user
# ------------------------------------------------------------
@pytest.fixture
def offline_user(viewer_user):
    # viewer_user is never marked present anywhere
    return viewer_user

# ------------------------------------------------------------
# Non-owner user
# ------------------------------------------------------------
@pytest.fixture
def non_owner_user(viewer_user):
    return viewer_user


# ------------------------------------------------------------
# Conflicted draft snapshot
# ------------------------------------------------------------
@pytest.fixture
def conflicted_draft_snapshot(
    db,
    draft_snapshot,
    owner_user,
):
    acquire_draft_lock(
        db=db,
        snapshot=draft_snapshot,
        user=owner_user,
    )
    return draft_snapshot

