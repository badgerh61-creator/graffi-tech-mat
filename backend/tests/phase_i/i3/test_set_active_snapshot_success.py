def test_set_active_snapshot_success(
    client,
    db,
    admin_user,
    project,
    completed_snapshot,
):
    response = client.post(
        "/mutations/set-active-snapshot",
        json={
            "projectId": project.id,
            "previousSnapshotId": None,
            "nextSnapshotId": completed_snapshot.id,
            "reason": "test",
        },
        headers={"Authorization": "Bearer test-token"},
    )

    assert response.status_code == 200

    db.refresh(project)
    assert project.active_snapshot_id == completed_snapshot.id

