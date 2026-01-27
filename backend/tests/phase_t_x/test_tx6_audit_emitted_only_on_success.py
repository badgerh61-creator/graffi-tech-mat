from app.studio import execute_tool
from app.models.audit import AuditLog

def test_audit_emitted_only_on_success(
    db,
    draft_snapshot,
    editor_user,
):
    execute_tool(
        db=db,
        user=editor_user,
        snapshot=draft_snapshot,
        station="geometry",
        tool="transform",
        operation="translate",
        params={"x": 1},
    )

    events = db.query(AuditLog).filter(
        AuditLog.action == "studio.tool.executed"
    ).all()

    assert len(events) == 1

