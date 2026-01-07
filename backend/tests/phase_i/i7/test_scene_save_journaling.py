from app.models.journal import JournalEntry
from app.models.rendered_snapshot import RenderedSnapshot

def test_scene_save_writes_journal_entry(
    client,
    db,
    scene,
    editor_user,
    valid_scene_state,
):
    response = client.post(
        f"/scenes/{scene.id}/mutations/save",
        json={"scene_state": valid_scene_state},
        headers=auth(editor_user),
    )

    snapshot_id = response.json()["snapshot_id"]

    entry = (
        db.query(JournalEntry)
        .filter_by(
            type="SAVE_SCENE",
            scene_id=scene.id,
            snapshot_id=snapshot_id,
        )
        .one()
    )

    assert entry.actor_user_id == editor_user.id
    assert entry.scene_hash is not None

