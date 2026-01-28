import pytest
from fastapi import HTTPException
from app.services.draft_lock_service import acquire_draft_lock


def test_draft_lock_conflict_rejected(
    db,
    draft_snapshot,
    editor_user,
    editor_user_without_tuning_capability,
):
    acquire_draft_lock(
        db=db,
        snapshot=draft_snapshot,
        user=editor_user,
    )

    with pytest.raises(HTTPException) as exc:
        acquire_draft_lock(
            db=db,
            snapshot=draft_snapshot,
            user=editor_user_without_tuning_capability,
        )

    assert exc.value.status_code == 409

