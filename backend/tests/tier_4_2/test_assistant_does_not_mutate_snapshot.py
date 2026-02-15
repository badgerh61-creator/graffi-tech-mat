from app.models.rendered_snapshot import RenderedSnapshot


def test_assistant_does_not_mutate_snapshot(
    client,
    db,
    draft_snapshot,
    editor_user,
):
    original_hash = draft_snapshot.scene_state_hash

    client.post(
        f"/snapshots/{draft_snapshot.id}/assistant/tuning",
        headers=auth(editor_user),
        json={"mode": "proposal"},
    )

    snapshot_after = db.query(RenderedSnapshot).get(draft_snapshot.id)

    assert snapshot_after.scene_state_hash == original_hash

