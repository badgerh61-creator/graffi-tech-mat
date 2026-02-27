def test_run_repro_endpoint(client, draft_snapshot, viewer_user, project):
    # create scenario first via 6S.6 template endpoint
    r1 = client.post(
        "/simulation/scenarios/from-template",
        json={
            "project_id": project.id,
            "name": "Baseline",
            "template_key": "accel_0_60_v1",
            "engine_version": "pseudo-v1",
            "overrides": {},
        },
        headers=auth(viewer_user),
    )
    assert r1.status_code == 200
    scenario_id = r1.json()["scenario_id"]

    # run it via 6S.5 /simulation/run
    r2 = client.post(
        "/simulation/run",
        json={"snapshot_id": draft_snapshot.id, "engine_version": "pseudo-v1", "scenario_id": scenario_id},
        headers=auth(viewer_user),
    )
    assert r2.status_code == 200
    run_id = r2.json()["run_id"]

    r3 = client.get(f"/simulation/runs/{run_id}/repro", headers=auth(viewer_user))
    assert r3.status_code == 200
    out = r3.json()
    assert out["run_id"] == run_id
    assert "run_fingerprint" in out
    assert out["engine_version"] == "pseudo-v1"
