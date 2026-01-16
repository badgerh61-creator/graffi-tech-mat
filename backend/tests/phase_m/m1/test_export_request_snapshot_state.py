def test_cannot_export_pending_snapshot(
    client,
    project,
    pending_snapshot,
    owner_user,
):
    response = client.post(
        "/exports/requests",
        json={
            "project_id": project.id,
            "snapshot_id": pending_snapshot.id,
            "export_type": "image",
            "options": {},
        },
        headers=auth(owner_user),
    )

    assert response.status_code == 409


def test_cannot_export_obsolete_snapshot(
    client,
    project,
    obsolete_snapshot,
    owner_user,
):
    response = client.post(
        "/exports/requests",
        json={
            "project_id": project.id,
            "snapshot_id": obsolete_snapshot.id,
            "export_type": "image",
            "options": {},
        },
        headers=auth(owner_user),
    )

    assert response.status_code == 409

