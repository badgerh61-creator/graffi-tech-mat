from app.kernel import acquire_draft_lock, release_draft_lock, handoff_draft_ownership
from app.services.presence_sessions import start_session

import pytest
from fastapi import HTTPException

def test_flow_blocked_on_session_expiry(
    db,
    draft_snapshot,
    editor_user,
):
    start_session(db=db, user=editor_user, project_id=draft_snapshot.project_id, ttl_seconds=1)
    advance_time(seconds=2)

    with pytest.raises(HTTPException):
        execute_tool(
            db=db,
            user=editor_user,
            snapshot=draft_snapshot,
            tool="translate",
            params={"x": 1},
        )

