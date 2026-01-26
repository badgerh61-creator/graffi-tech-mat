from app.services.panel_segmenter import segment_panels
from app.models.audit_log import AuditLog

def test_panel_segmentation_emits_audit_event(
    db,
    surfaced_draft_snapshot,
    editor_user,
):
    new_snapshot = segment_panels(
        db=db,
        snapshot=surfaced_draft_snapshot,
        user=editor_user,
        panels=[{
            "type": "side",
            "surface_ids": ["surface-1"],
            "label": "left-side",
        }],
    )

    events = db.query(AuditLog).filter(
        AuditLog.action == "panel.segmented",
        AuditLog.resource_id == new_snapshot.id,
    ).all()

    assert len(events) == 1

