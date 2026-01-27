import pytest
from fastapi import HTTPException

from app.services.snapshot_mutations import apply_transform

def test_concurrent_mutation_blocked(
    db,
    draft_snapshot_owned_by_user_a,
    user_b,
):
    with pytest.raises(HTTPException):
        apply_transform(
            db=db,
            snapshot=draft_snapshot_owned_by_user_a,
            user=user_b,
            operation="scale",
            target_id="panel-1",
            params={"factor": 2},
        )

