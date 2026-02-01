from app.kernel import acquire_draft_lock, release_draft_lock, handoff_draft_ownership
from app.services.presence_sessions import start_session

import pytest
from fastapi import HTTPException

def test_tool_blocked_on_conflict(
    db,
    conflicted_draft_snapshot,
    owner_user,
):
    acquire_draft_lock(db=db, snapshot=conflicted_draft_snapshot, user=owner_user)

    with pytest.raises(HTTPException) as exc:
        execute_tool(
            db=db,
            user=owner_user,
            snapshot=conflicted_draft_snapshot,
            tool="scale",
            params={"factor": 1.2},
        )

    assert exc.value.status_code == 409

