def test_export_draft_snapshot_rejected(
    client,
    draft_snapshot,
    editor_user,
):
    response = client.post(
        "/exports/images",
        headers=auth(editor_user),
        json={
            "snapshot_id": draft_snapshot.id,
            "format": "png",
            "resolution": "high",
        },
    )

    assert response.status_code == 409

