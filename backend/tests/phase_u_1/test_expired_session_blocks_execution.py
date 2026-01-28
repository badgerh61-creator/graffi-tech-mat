from app.services.transform_executor import apply_transform
import pytest
from fastapi import HTTPException

from app.services.presence_sessions import start_session
from tests.phase_u_1.time_helpers import advance_time
from datetime import datetime, timedelta

def test_expired_session_blocks_execution(
    db,
    draft_snapshot,
    editor_user,
    monkeypatch,
):
    start_session(
        db=db,
        user=editor_user,
        project_id=draft_snapshot.project_id,
        ttl_seconds=1,
    )

    future = datetime.utcnow() + timedelta(seconds=2)

    monkeypatch.setattr(
        "app.services.presence_sessions.datetime",
        type(
            "FrozenDatetime",
            (),
            {"utcnow": staticmethod(lambda: future)},
        ),
    )

    with pytest.raises(HTTPException):
        apply_transform(
            db=db,
            snapshot=draft_snapshot,
            user=editor_user,
            operation="translate",
            target_id="panel-1",
            params={"x": 1},
        )

