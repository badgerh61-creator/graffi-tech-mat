def test_viewer_cannot_set_engine_tune(
    client,
    viewer_user,
    completed_snapshot,
):
    auth(viewer_user)

    response = client.post(
        "/mutations/tuning/set-engine-tune",
        json={
            "project_id": completed_snapshot.project_id,
            "snapshot_base_id": completed_snapshot.id,
            "preset_id": "sport",
        },
    )

    assert response.status_code == 403

