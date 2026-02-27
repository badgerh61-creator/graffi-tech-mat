def test_sim_job_creates_artifact(client, draft_snapshot, viewer_user):
    r = client.post(
        "/simulation/jobs",
        json={
            "snapshot_id": draft_snapshot.id,
            "scenario": {"duration_s": 1.0, "timestep_s": 0.5, "throttle": 0.6},
            "engine_version": "pseudo-v1",
        },
        headers=auth(viewer_user),
    )
    assert r.status_code == 200
    data = r.json()
    assert data["job_id"] > 0
    assert data["status"] in ("succeeded", "running", "queued", "failed")
    assert data["artifact_id"] is not None
