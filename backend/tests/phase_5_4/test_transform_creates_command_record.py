from app.services.snapshot_mutations import apply_transform
from app.models.audit_log import AuditLog

def test_transform_creates_command_record(
    db,
    draft_snapshot,
    editor_user,
):
    new_snapshot = apply_transform(
        db=db,
        snapshot=draft_snapshot,
        user=editor_user,
        operation="scale",
        target_id="panel-1",
        params={"factor": 1.2},
    )

    events = (
        db.query(AuditLog)
        .filter(AuditLog.action == "snapshot.transform")
        .filter(AuditLog.resource_id == new_snapshot.id)
        .all()
    )

    assert len(events) == 1

