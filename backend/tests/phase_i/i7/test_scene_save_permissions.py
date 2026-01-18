from app.models.journal_entry import JournalEntry
from app.models.rendered_snapshot import RenderedSnapshot


def test_viewer_cannot_save_scene(
    client,
    scene,
    viewer_user,
    valid_scene_state,
    request,
):
    # 🔑 Explicitly force viewer for this test
    request.node.user = viewer_user

    response = client.post(
        f"/scenes/{scene.id}/mutations/save",
        json={"scene_state": valid_scene_state},
        headers=auth(viewer_user),
    )

    assert response.status_code == 403

