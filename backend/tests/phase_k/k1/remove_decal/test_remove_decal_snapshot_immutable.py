from app.models.rendered_snapshot import RenderedSnapshot

def test_remove_decal_creates_new_snapshot(
    client,
    db,
    project,
    completed_snapshot_with_decal,
    editor_user,
):
    response = client.post(
        "/mutations/decor/exterior/remove-decal",
        json={
            "project_id": project.id,
            "snapshot_base_id": completed_snapshot_with_decal.id,
            "decal_instance_id": "abc123",
        },
        headers=auth(editor_user),
    )

    assert response.status_code == 200
    new_snapshot_id = response.json()["snapshot_id"]

    assert new_snapshot_id != completed_snapshot_with_decal.id

    base = db.get(RenderedSnapshot, completed_snapshot_with_decal.id)
    new = db.get(RenderedSnapshot, new_snapshot_id)

    assert len(base.payload["decor"]["decals"]) == 1
    assert len(new.payload["decor"]["decals"]) == 0

