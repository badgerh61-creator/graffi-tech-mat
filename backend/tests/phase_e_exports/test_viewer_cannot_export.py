def test_viewer_cannot_export(
    client,
    completed_snapshot,
    viewer_user,
):
    response = client.post(
        "/exports/images",
        headers=auth(viewer_user),
        json={
            "snapshot_id": completed_snapshot.id,
            "format": "png",
            "resolution": "low",
        },
    )

    assert response.status_code == 403

