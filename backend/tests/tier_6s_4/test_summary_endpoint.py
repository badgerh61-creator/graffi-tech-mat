def test_summary_endpoint(client, draft_snapshot, viewer_user):
    r1 = client.post(
        "/simulation/jobs",
        json={"snapshot_id": draft_snapshot.id, "scenario": {"duration_s": 1.0, "timestep_s": 0.5}},
        headers=auth(viewer_user),
    )
    assert r1.status_code == 200
    artifact_id = r1.json()["artifact_id"]
    assert artifact_id is not None

    r2 = client.get(f"/simulation/artifacts/{artifact_id}/summary", headers=auth(viewer_user))
    assert r2.status_code == 200
    data = r2.json()
    assert data["artifact_id"] == artifact_id
    assert "summary" in data
    assert "speed_max_mps" in data["summary"]
