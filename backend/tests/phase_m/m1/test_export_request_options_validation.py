def test_invalid_export_type_rejected(
    client,
    project,
    completed_snapshot,
    owner_user,
):
    response = client.post(
        "/exports/requests",
        json={
            "project_id": project.id,
            "snapshot_id": completed_snapshot.id,
            "export_type": "gif",
            "options": {},
        },
        headers=auth(owner_user),
    )

    assert response.status_code == 400


def test_invalid_options_schema_rejected(
    client,
    project,
    completed_snapshot,
    owner_user,
):
    response = client.post(
        "/exports/requests",
        json={
            "project_id": project.id,
            "snapshot_id": completed_snapshot.id,
            "export_type": "image",
            "options": {"dpi": 300},
        },
        headers=auth(owner_user),
    )

    assert response.status_code == 400

