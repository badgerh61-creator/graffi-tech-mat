def test_metrics_viewer_can_access(
    client,
    draft_snapshot,
    viewer_user,
):
    r = client.get(
        f"/snapshots/{draft_snapshot.id}/metrics/performance",
        headers=auth(viewer_user),
    )
    assert r.status_code == 200

