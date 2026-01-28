import pytest
from fastapi import HTTPException
from app.services.draft_lock_service import acquire_draft_lock


def test_completed_snapshot_cannot_be_locked(
    db,
    completed_snapshot,
    editor_user,
):
    with pytest.raises(HTTPException) as exc:
        acquire_draft_lock(
            db=db,
            snapshot=completed_snapshot,
            user=editor_user,
        )

    assert exc.value.status_code == 409

