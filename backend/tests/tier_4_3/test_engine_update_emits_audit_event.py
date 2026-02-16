from datetime import datetime, timedelta

from app.services.tool_executor import execute_tool
from app.models.audit_log import AuditLog
from app.models.presence_session import PresenceSession


def test_tuning_update_audited(
    db,
    draft_snapshot,
    owner_user,
):
    # ✅ Create active session (required by ToolExecutor)
    session = PresenceSession(
        user_id=owner_user.id,
        project_id=draft_snapshot.project_id,
        expires_at=datetime.utcnow() + timedelta(minutes=30),
    )
    db.add(session)
    db.commit()

    new_snapshot = execute_tool(
        db=db,
        user=owner_user,
        snapshot=draft_snapshot,
        tool="UPDATE_ENGINE_CONFIG",
        params={"preset_id": "sport"},
    )

    event = (
        db.query(AuditLog)
        .filter(AuditLog.resource_id == new_snapshot.id)
        .filter(AuditLog.action == "snapshot.tuning_updated")
        .first()
    )

    assert event is not None

