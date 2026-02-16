def test_metrics_are_deterministic(
    client,
    draft_snapshot,
    viewer_user,
):
    r1 = client.get(
        f"/snapshots/{draft_snapshot.id}/metrics/performance",
        headers=auth(viewer_user),
    )
    r2 = client.get(
        f"/snapshots/{draft_snapshot.id}/metrics/performance",
        headers=auth(viewer_user),
    )

    assert r1.status_code == 200
    assert r1.json() == r2.json()

