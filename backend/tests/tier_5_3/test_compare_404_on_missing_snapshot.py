def test_compare_404_on_missing_snapshot(client, viewer_user):
    r = client.get(
        "/testing/compare?snapshot_a=999999&snapshot_b=1&scenario_id=track-dry-day-v1",
        headers=auth(viewer_user),
    )
    assert r.status_code == 404
