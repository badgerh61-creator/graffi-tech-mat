def test_cannot_export_from_archived_project(
    client,
    archived_project,
    archived_project_snapshot,
    owner_user,
):
    response = client.post(
        "/exports/requests",
        json={
            "project_id": archived_project.id,
            "snapshot_id": archived_project_snapshot.id,
            "export_type": "image",
            "options": {},
        },
        headers=auth(owner_user),
    )

    assert response.status_code == 403

