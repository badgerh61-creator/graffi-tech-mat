from app.models.journal_entry import JournalEntry
from app.models.rendered_snapshot import RenderedSnapshot

def test_scene_save_does_not_mutate_existing_snapshots(
    client,
    db,
    scene,
    existing_snapshot,
    editor_user,
    valid_scene_state,
):
    old_status = existing_snapshot.status

    client.post(
        f"/scenes/{scene.id}/mutations/save",
        json={"scene_state": valid_scene_state},
        headers=auth(editor_user),
    )

    db.refresh(existing_snapshot)
    assert existing_snapshot.status == old_status

