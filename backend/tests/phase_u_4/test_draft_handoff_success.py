import pytest
from fastapi import HTTPException

import app.services.presence_service as presence_service
from app.services.draft_lock_service import acquire_draft_lock
from app.services.draft_handoff_service import handoff_draft_ownership


def test_draft_handoff_success(
    db,
    draft_snapshot,
    owner_user,
    editor_user,
):
    # 🔑 REQUIRED: mark presence in presence_service
    presence_service.mark_user_present(editor_user)

    acquire_draft_lock(
        db=db,
        snapshot=draft_snapshot,
        user=owner_user,
    )

    result = handoff_draft_ownership(
        db=db,
        snapshot=draft_snapshot,
        from_user=owner_user,
        to_user=editor_user,
    )

    assert result.user_id == editor_user.id

