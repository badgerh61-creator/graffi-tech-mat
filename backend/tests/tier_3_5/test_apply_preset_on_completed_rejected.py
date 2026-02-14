import pytest
from fastapi import HTTPException

def test_apply_preset_on_completed_rejected(
    db,
    completed_snapshot,
    decor_preset,
    owner_user,
):
    with pytest.raises(HTTPException) as exc:
        apply_decor_preset(
            db=db,
            snapshot=completed_snapshot,
            preset=decor_preset,
            user=owner_user,
        )

    assert exc.value.status_code == 409

