import pytest
from fastapi import HTTPException

import app.services.presence_service as presence_service
from app.services.transform_executor import apply_transform
from app.services.draft_lock_service import acquire_draft_lock
from app.kernel import handoff_draft_ownership


def test_previous_owner_loses_authority(
    db,
    locked_draft_snapshot,
    owner_user,
    editor_user,
):
    presence_service.mark_user_present(editor_user)

    handoff_draft_ownership(
        db=db,
        snapshot=locked_draft_snapshot,
        from_user=owner_user,
        to_user=editor_user,
    )

    with pytest.raises(HTTPException):
        apply_transform(
            db=db,
            snapshot=locked_draft_snapshot,
            user=owner_user,
            operation="translate",
            target_id="panel-1",
            params={"x": 1},
        )

