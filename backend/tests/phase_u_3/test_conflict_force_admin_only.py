import pytest
from fastapi import HTTPException

from app.services import resolve_conflict
from app.services.conflict_detector import detect_conflict
from app.services.transform_executor import apply_transform

def test_conflict_force_admin_only(
    db,
    conflicted_draft_snapshot,
    editor_user,
):
    with pytest.raises(HTTPException) as exc:
        resolve_conflict(
            db=db,
            snapshot=conflicted_draft_snapshot,
            user=editor_user,
            strategy="force",
        )

    assert exc.value.status_code == 403

