from app.models.journal_entry import JournalEntry
from app.models.rendered_snapshot import RenderedSnapshot

def test_scene_save_is_deterministic(
    client,
    db,
    scene,
    editor_user,
    valid_scene_state,
):
    first = client.post(
        f"/scenes/{scene.id}/mutations/save",
        json={"scene_state": valid_scene_state},
        headers=auth(editor_user),
    )

    second = client.post(
        f"/scenes/{scene.id}/mutations/save",
        json={"scene_state": valid_scene_state},
        headers=auth(editor_user),
    )

    assert first.status_code == 200
    assert second.status_code == 200

    assert first.json()["snapshot_id"] == second.json()["snapshot_id"]

