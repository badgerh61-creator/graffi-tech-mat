from app.models.journal import JournalEntry
from app.models.rendered_snapshot import RenderedSnapshot
from app.models.rendered_snapshot import RenderedSnapshot as Snapshot

def test_scene_save_creates_snapshot_and_job(
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

    assert response.status_code == 200

    data = response.json()
    assert "snapshot_id" in data

    snapshot = db.get(Snapshot, data["snapshot_id"])
    assert snapshot is not None
    assert snapshot.status == "pending"

