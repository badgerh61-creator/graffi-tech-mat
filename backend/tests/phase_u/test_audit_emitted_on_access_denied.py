from app.services.snapshot_mutations import apply_transform
from fastapi import HTTPException
import pytest

def test_audit_emitted_on_access_denied(
    db,
    draft_snapshot_owned_by_user_a,
    user_b,
):
    with pytest.raises(HTTPException):
        apply_transform(
            db=db,
            snapshot=draft_snapshot_owned_by_user_a,
            user=user_b,
            operation="translate",
            target_id="panel-1",
            params={"x": 1},
        )

    events = get_audit_events(action="snapshot.access_denied")
    assert len(events) == 1

