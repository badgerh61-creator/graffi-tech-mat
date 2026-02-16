import pytest
from fastapi import HTTPException
from app.services.tuning_mutation import update_engine_config

def test_tuning_requires_lock(
    db,
    draft_snapshot,
    non_owner_user,
):
    with pytest.raises(HTTPException):
        update_engine_config(
            db=db,
            snapshot=draft_snapshot,
            user=non_owner_user,
            payload={"boost": 1.2},
        )

