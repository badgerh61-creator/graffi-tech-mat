import pytest
from fastapi import HTTPException

def test_abandoned_draft_cannot_finalize(
    db,
    abandoned_snapshot,
    editor_user,
):
    with pytest.raises(HTTPException) as exc:
        finalize_snapshot(
            db=db,
            snapshot=abandoned_snapshot,
            user=editor_user,
        )

    assert exc.value.status_code == 409

