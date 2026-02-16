from datetime import datetime, timedelta
from app.services.tool_executor import execute_tool
from app.models.presence_session import PresenceSession


def test_engine_update_creates_child_snapshot(
    db,
    draft_snapshot,
    owner_user,
):
    # ✅ Create active session
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

    assert new_snapshot.id != draft_snapshot.id
    assert new_snapshot.parent_snapshot_id == draft_snapshot.id
    assert new_snapshot.status == "draft"

