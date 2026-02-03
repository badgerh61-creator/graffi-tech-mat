from app.models.snapshot import Snapshot

def test_studio_state_has_no_side_effects(
    db,
    client,
    editor_user,
):
    snapshot_count_before = db.query(Snapshot).count()

    client.get("/studio/state", headers=auth(editor_user))

    snapshot_count_after = db.query(Snapshot).count()
    assert snapshot_count_before == snapshot_count_after

