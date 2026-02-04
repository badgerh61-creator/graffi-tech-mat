def test_export_completed_snapshot_success(
    client,
    completed_snapshot,
    editor_user,
):
    response = client.post(
        "/exports/images",
        headers=auth(editor_user),
        json={
            "snapshot_id": completed_snapshot.id,
            "format": "png",
            "resolution": "medium",
        },
    )

    assert response.status_code == 200
    assert response.json()["status"] == "queued"
