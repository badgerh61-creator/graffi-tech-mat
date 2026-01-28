import pytest
from fastapi import HTTPException

from app.services.draft_lock_service import acquire_draft_lock
from app.services.transform_executor import apply_transform


def test_non_owner_mutation_rejected(
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
        apply_transform(
            db=db,
            snapshot=draft_snapshot,
            user=editor_user_without_tuning_capability,
            operation="translate",
            target_id="panel-1",
            params={"x": 1},
        )

    assert exc.value.status_code == 403

