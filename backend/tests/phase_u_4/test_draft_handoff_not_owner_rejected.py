import pytest
from fastapi import HTTPException

import app.services.presence_service as presence_service
from app.services.draft_lock_service import acquire_draft_lock
from app.services.draft_handoff_service import handoff_draft_ownership


def test_draft_handoff_not_owner_rejected(
    db,
    draft_snapshot,
    owner_user,
    viewer_user,
):
    presence_service.mark_user_present(owner_user)

    acquire_draft_lock(
        db=db,
        snapshot=draft_snapshot,
        user=owner_user,
    )

    with pytest.raises(HTTPException) as exc:
        handoff_draft_ownership(
            db=db,
            snapshot=draft_snapshot,
            from_user=viewer_user,
            to_user=owner_user,
        )

    assert exc.value.status_code == 403

