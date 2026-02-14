def test_tuning_readonly_on_completed_snapshot(
    client,
    completed_snapshot,
    viewer_user,
):
    response = client.get(
        f"/snapshots/{completed_snapshot.id}/tuning",
        headers=auth(viewer_user),
    )

    assert response.status_code == 200

