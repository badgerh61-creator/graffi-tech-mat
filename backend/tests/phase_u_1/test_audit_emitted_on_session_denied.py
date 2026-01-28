import pytest
from fastapi import HTTPException

from app.services.transform_executor import apply_transform


def test_audit_emitted_on_session_denied(
    db,
    draft_snapshot,
    editor_user,
):
    try:
        apply_transform(
            db=db,
            snapshot=draft_snapshot,
            user=editor_user,
            operation="translate",
            target_id="panel-1",
            params={"x": 1},
        )
    except HTTPException:
        pass

    events = get_audit_events(action="session.denied")
    assert len(events) == 1

