def test_viewer_cannot_set_brakes(client, viewer_user, completed_snapshot):
    auth(viewer_user)

    res = client.post(
        "/mutations/tuning/set-brakes",
        json={
            "project_id": completed_snapshot.project_id,
            "snapshot_base_id": completed_snapshot.id,
            "preset_id": "sport",
        },
    )

    assert res.status_code == 403

