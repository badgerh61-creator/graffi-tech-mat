def test_viewer_cannot_create_draft(
    client,
    completed_snapshot,
    viewer_user,
):
    res = client.post(
        f"/snapshots/{completed_snapshot.id}/draft",
        headers=auth(viewer_user),
    )

    assert res.status_code == 403

