import pytest
from fastapi import HTTPException
from app.services.tuning_mutation import update_engine_config

def test_completed_snapshot_rejected(
    db,
    completed_snapshot,
    owner_user,
):
    with pytest.raises(HTTPException):
        update_engine_config(
            db=db,
            snapshot=completed_snapshot,
            user=owner_user,
            payload={"boost": 1.2},
        )

