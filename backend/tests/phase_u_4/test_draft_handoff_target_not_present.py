import pytest
from fastapi import HTTPException

from app.services.draft_lock_service import acquire_draft_lock
from app.kernel import handoff_draft_ownership


def test_draft_handoff_target_not_present(
    db,
    locked_draft_snapshot,
    owner_user,
    offline_user,
):
    with pytest.raises(HTTPException) as exc:
        handoff_draft_ownership(
            db=db,
            snapshot=locked_draft_snapshot,
            from_user=owner_user,
            to_user=offline_user,
        )

    assert exc.value.status_code == 409

