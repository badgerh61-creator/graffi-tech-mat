from app.kernel import acquire_draft_lock, release_draft_lock, handoff_draft_ownership
from app.services.presence_sessions import start_session

import pytest
from fastapi import HTTPException

def test_tool_blocked_without_draft_ownership(
    db,
    draft_snapshot,
    owner_user,
    non_owner_user,
):
    acquire_draft_lock(db=db, snapshot=draft_snapshot, user=owner_user)

    with pytest.raises(HTTPException) as exc:
        execute_tool(
            db=db,
            user=non_owner_user,
            snapshot=draft_snapshot,
            tool="translate",
            params={"x": 1},
        )

    assert exc.value.status_code == 403

