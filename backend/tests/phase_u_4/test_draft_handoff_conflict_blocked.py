import pytest
from fastapi import HTTPException

from app.services.draft_handoff_service import handoff_draft_ownership


def test_draft_handoff_conflict_blocked(
    db,
    conflicted_draft_snapshot,
    owner_user,
    editor_user,
):
    with pytest.raises(HTTPException) as exc:
        handoff_draft_ownership(
            db=db,
            snapshot=conflicted_draft_snapshot,
            from_user=owner_user,
            to_user=editor_user,
        )

    assert exc.value.status_code == 409

