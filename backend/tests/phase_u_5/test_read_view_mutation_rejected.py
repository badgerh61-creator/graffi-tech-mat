import pytest
from fastapi import HTTPException


def test_read_view_mutation_rejected(
    db,
    draft_snapshot,
    viewer_user,
    start_session_fn,
    open_read_view_fn,
    execute_tool_fn,
):
    start_session_fn(
        db=db,
        user=viewer_user,
        project_id=draft_snapshot.project_id,
    )

    open_read_view_fn(
        db=db,
        snapshot=draft_snapshot,
        user=viewer_user,
    )

    with pytest.raises(HTTPException) as exc:
        execute_tool_fn(
            db=db,
            user=viewer_user,
            snapshot=draft_snapshot,
            tool="scale",
            params={"factor": 2},
        )

    assert exc.value.status_code == 403

