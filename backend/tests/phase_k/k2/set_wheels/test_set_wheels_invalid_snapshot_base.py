def test_set_wheels_invalid_snapshot_base(
    client,
    project,
    failed_snapshot,
    editor_user,
):
    response = client.post(
        "/mutations/tuning/set-wheels",
        json={
            "project_id": project.id,
            "snapshot_base_id": failed_snapshot.id,
            "diameter": 18,
            "width": 8,
            "offset": 40,
        },
        headers=auth(editor_user),
    )

    assert response.status_code == 409
    assert response.json()["error"] == "invalid_snapshot_base"

