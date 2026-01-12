def test_set_suspension_creates_new_snapshot(
    client,
    db,
    project,
    completed_snapshot,
    editor_user,
):
    response = client.post(
        "/mutations/tuning/set-suspension",
        json={
            "project_id": project.id,
            "snapshot_base_id": completed_snapshot.id,
            "preset_id": "sport_low",
        },
        headers=auth(editor_user),
    )

    assert response.status_code == 200

    new_snapshot_id = response.json()["snapshot_id"]
    assert new_snapshot_id != completed_snapshot.id

    base_snapshot = db.get(type(completed_snapshot), completed_snapshot.id)
    new_snapshot = db.get(type(completed_snapshot), new_snapshot_id)

    assert base_snapshot.payload != new_snapshot.payload

