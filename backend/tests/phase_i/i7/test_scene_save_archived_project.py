from app.models.journal import JournalEntry
from app.models.rendered_snapshot import RenderedSnapshot

def test_cannot_save_scene_in_archived_project(
    client,
    archived_scene,
    owner_user,
    valid_scene_state,
):
    response = client.post(
        f"/scenes/{archived_scene.id}/mutations/save",
        json={"scene_state": valid_scene_state},
        headers=auth(owner_user),
    )

    assert response.status_code == 403

