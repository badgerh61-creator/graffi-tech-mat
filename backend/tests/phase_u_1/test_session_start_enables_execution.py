from app.services.transform_executor import apply_transform
import pytest
from fastapi import HTTPException
from app.services.presence_sessions import start_session

def test_session_start_enables_execution(
    db,
    draft_snapshot,
    editor_user,
):
    start_session(
        db=db,
        user=editor_user,
        project_id=draft_snapshot.project_id,
    )

    new_snapshot = apply_transform(
        db=db,
        snapshot=draft_snapshot,
        user=editor_user,
        operation="translate",
        target_id="panel-1",
        params={"x": 2},
    )

    assert new_snapshot is not None

