def test_metrics_missing_inputs_degrades_confidence(
    client,
    snapshot_with_empty_tuning,
    viewer_user,
):
    r = client.get(
        f"/snapshots/{snapshot_with_empty_tuning.id}/metrics/performance",
        headers=auth(viewer_user),
    )
    assert r.status_code == 200
    data = r.json()
    assert data["confidence"] < 1.0
    assert len(data["notes"]) >= 1

