def test_compare_returns_metrics_and_deltas(client, existing_snapshot, draft_snapshot, viewer_user):
    a = existing_snapshot
    b = draft_snapshot

    r = client.get(
        f"/testing/compare?snapshot_a={a.id}&snapshot_b={b.id}&scenario_id=track-dry-day-v1",
        headers=auth(viewer_user),
    )
    assert r.status_code == 200
    data = r.json()

    assert "a" in data and "b" in data
    assert data["a"]["snapshot_id"] == a.id
    assert data["b"]["snapshot_id"] == b.id

    assert "deltas" in data
    assert "metrics_delta" in data["deltas"]
