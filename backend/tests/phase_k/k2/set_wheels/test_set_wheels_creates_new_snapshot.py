def test_set_wheels_creates_new_snapshot(
    client,
    db,
    project,
    completed_snapshot,
    editor_user,
):
    response = client.post(
        "/mutations/tuning/set-wheels",
        json={
            "project_id": project.id,
            "snapshot_base_id": completed_snapshot.id,
            "diameter": 19,
            "width": 9.5,
            "offset": 35,
        },
        headers=auth(editor_user),
    )

    assert response.status_code == 200
    new_snapshot_id = response.json()["snapshot_id"]

    assert new_snapshot_id != completed_snapshot.id

    base = db.get(type(completed_snapshot), completed_snapshot.id)
    new = db.get(type(completed_snapshot), new_snapshot_id)

    assert base.payload != new.payload

