import pytest
from fastapi import HTTPException

def test_apply_preset_requires_draft_lock(
    db,
    draft_snapshot,
    decor_preset,
    non_owner_user,
):
    with pytest.raises(HTTPException) as exc:
        apply_decor_preset(
            db=db,
            snapshot=draft_snapshot,
            preset=decor_preset,
            user=non_owner_user,
        )

    assert exc.value.status_code == 403

