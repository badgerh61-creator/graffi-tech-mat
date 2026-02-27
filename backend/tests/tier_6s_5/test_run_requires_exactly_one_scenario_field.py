def test_run_requires_exactly_one_scenario_field(client, draft_snapshot, viewer_user):
    r = client.post(
        "/simulation/run",
        json={
            "snapshot_id": draft_snapshot.id,
            "engine_version": "pseudo-v1",
            "scenario_id": 1,
            "scenario": {"throttle": 0.5},
        },
        headers=auth(viewer_user),
    )
    assert r.status_code == 422
