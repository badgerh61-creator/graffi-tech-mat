def test_metrics_snapshot_not_found_404(
    client,
    viewer_user,
):
    r = client.get(
        "/snapshots/999999/metrics/performance",
        headers=auth(viewer_user),
    )
    assert r.status_code == 404

