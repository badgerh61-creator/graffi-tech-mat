import pytest
from fastapi import HTTPException

import app.services.presence_service as presence_service
from app.services.draft_lock_service import acquire_draft_lock
from app.services.draft_handoff_service import handoff_draft_ownership
from app.services.transform_executor import apply_transform


def test_previous_owner_loses_authority(
    db,
    draft_snapshot,
    owner_user,
    editor_user,
):
    # 🔑 REQUIRED: mark presence
    presence_service.mark_user_present(editor_user)

    acquire_draft_lock(
        db=db,
        snapshot=draft_snapshot,
        user=owner_user,
    )

    handoff_draft_ownership(
        db=db,
        snapshot=draft_snapshot,
        from_user=owner_user,
        to_user=editor_user,
    )

    # Old owner must now be blocked
    with pytest.raises(HTTPException):
        apply_transform(
            db=db,
            snapshot=draft_snapshot,
            user=owner_user,
            operation="translate",
            target_id="panel-1",
            params={"x": 1},
        )

