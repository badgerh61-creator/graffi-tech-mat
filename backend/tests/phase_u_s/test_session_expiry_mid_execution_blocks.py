import pytest
from app.services.time_test_utils import advance_time
from app.services.kernel_test_facade import *

def test_session_expiry_mid_execution_blocks(
    db,
    draft_snapshot,
    editor_user,
):
    start_session(db=db, user=editor_user, project_id=draft_snapshot.project_id, ttl_seconds=1)
    advance_time(seconds=2)

    with pytest.raises(Exception):
        execute_tool(
            db=db,
            user=editor_user,
            snapshot=draft_snapshot,
            tool="translate",
            params={"x": 1},
        )

