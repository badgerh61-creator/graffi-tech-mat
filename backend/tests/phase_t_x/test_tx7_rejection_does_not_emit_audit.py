import pytest
from app.models.audit import AuditLog
from app.studio import execute_tool

def test_rejection_does_not_emit_audit(
    db,
    completed_snapshot,
    editor_user,
):
    with pytest.raises(Exception):
        execute_tool(
            db=db,
            user=editor_user,
            snapshot=completed_snapshot,
            station="geometry",
            tool="transform",
            operation="translate",
            params={"x": 1},
        )

    events = db.query(AuditLog).filter(
        AuditLog.action == "studio.tool.executed"
    ).all()

    assert len(events) == 0

