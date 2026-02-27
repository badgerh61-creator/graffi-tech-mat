def test_batch_runs_create_artifacts_and_run_index(client, draft_snapshot, viewer_user):
    r = client.post(
        "/simulation/batches",
        json={
            "snapshot_id": draft_snapshot.id,
            "engine_version": "pseudo-v1",
            "template_keys": ["accel_0_60_v1", "thermal_load_v1"],
        },
        headers=auth(viewer_user),
    )
    assert r.status_code == 200
    out = r.json()
    assert out["batch_id"] > 0
    assert out["status"] in ("succeeded", "running")
    assert len(out["artifact_ids"]) == 2
    assert len(out["run_ids"]) == 2
