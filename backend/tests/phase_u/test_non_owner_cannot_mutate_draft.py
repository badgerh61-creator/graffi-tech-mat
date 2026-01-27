import pytest
from fastapi import HTTPException

from app.services.snapshot_mutations import apply_transform

def test_non_owner_cannot_mutate_draft(
    db,
    draft_snapshot_owned_by_user_a,
    user_b,
):
    with pytest.raises(HTTPException) as exc:
        apply_transform(
            db=db,
            snapshot=draft_snapshot_owned_by_user_a,
            user=user_b,
            operation="translate",
            target_id="panel-1",
            params={"x": 1},
        )

    assert exc.value.status_code == 403

