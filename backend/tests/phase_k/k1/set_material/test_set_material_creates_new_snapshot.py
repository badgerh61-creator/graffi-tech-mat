from app.models.rendered_snapshot import RenderedSnapshot

def test_set_material_creates_new_snapshot(
    client,
    db,
    project,
    completed_snapshot,
    editor_user,
):
    response = client.post(
        "/mutations/decor/exterior/set-material",
        json={
            "project_id": project.id,
            "snapshot_base_id": completed_snapshot.id,
            "panel": "door_left",
            "material": {
                "material_id": "mat_1",
                "parameters": {
                    "color": "#123456",
                    "finish": "metallic",
                },
            },
        },
        headers=auth(editor_user),
    )

    assert response.status_code == 200
    new_snapshot_id = response.json()["snapshot_id"]

    assert new_snapshot_id != completed_snapshot.id

    base = db.get(RenderedSnapshot, completed_snapshot.id)
    new = db.get(RenderedSnapshot, new_snapshot_id)

    assert base.payload != new.payload

