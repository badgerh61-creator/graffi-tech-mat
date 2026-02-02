import pytest
from app.services.kernel_test_facade import *

def test_conflict_detection_under_concurrent_updates(
    db,
    conflicted_draft_snapshot,
    owner_user,
):
    acquire_draft_lock(db=db, snapshot=conflicted_draft_snapshot, user=owner_user)

    with pytest.raises(Exception):
        execute_tool(
            db=db,
            user=owner_user,
            snapshot=conflicted_draft_snapshot,
            tool="translate",
            params={"x": 10},
        )

