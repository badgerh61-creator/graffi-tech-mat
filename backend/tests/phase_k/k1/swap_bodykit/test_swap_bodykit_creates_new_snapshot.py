from app.models.rendered_snapshot import RenderedSnapshot

def test_swap_bodykit_creates_new_snapshot(
    client,
    db,
    project,
    completed_snapshot,
    editor_user,
):
    response = client.post(
        "/mutations/decor/exterior/swap-bodykit",
        json={
            "project_id": project.id,
            "snapshot_base_id": completed_snapshot.id,
            "bodykit_id": "bk_1",
        },
        headers=auth(editor_user),
    )

    assert response.status_code == 200
    new_snapshot_id = response.json()["snapshot_id"]

    assert new_snapshot_id != completed_snapshot.id

    base = db.get(RenderedSnapshot, completed_snapshot.id)
    new = db.get(RenderedSnapshot, new_snapshot_id)

    assert base.payload != new.payload

