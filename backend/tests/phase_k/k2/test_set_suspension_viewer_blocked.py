def test_viewer_cannot_set_tuning(client, viewer_user, project, completed_snapshot):
    response = client.post(
        "/mutations/tuning/set-suspension",
        json={
            "project_id": project.id,
            "snapshot_base_id": completed_snapshot.id,
            "preset_id": "sport_low",
        },
        headers=auth(viewer_user),
    )

    assert response.status_code == 403

