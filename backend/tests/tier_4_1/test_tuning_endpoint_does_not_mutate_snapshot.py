from app.models.rendered_snapshot import RenderedSnapshot

def test_tuning_endpoint_does_not_mutate_snapshot(
    db,
    client,
    draft_snapshot,
    editor_user,
):
    original_id = draft_snapshot.id

    client.get(
        f"/snapshots/{draft_snapshot.id}/tuning",
        headers=auth(editor_user),
    )

    snapshot_after = db.query(RenderedSnapshot).get(original_id)

    assert snapshot_after.id == original_id

