from app.services.snapshot_resolver import resolve_active_snapshot_for_boot

def test_editor_boot_uses_fallback_when_active_snapshot_is_obsolete(
    db,
    project,
    obsolete_snapshot,
    completed_snapshot,
):
    project.active_snapshot_id = obsolete_snapshot.id
    db.commit()

    # simulate editor boot resolution logic
    resolved_snapshot = resolve_active_snapshot_for_boot(db, project.id)

    assert resolved_snapshot.id == completed_snapshot.id
    assert resolved_snapshot.status == "completed"

