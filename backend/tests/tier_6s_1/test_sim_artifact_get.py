def test_sim_artifact_get(client, draft_snapshot, viewer_user):
    r1 = client.post(
        "/simulation/jobs",
        json={"snapshot_id": draft_snapshot.id, "scenario": {"duration_s": 1.0, "timestep_s": 0.5}},
        headers=auth(viewer_user),
    )
    assert r1.status_code == 200
    artifact_id = r1.json()["artifact_id"]
    assert artifact_id is not None

    r2 = client.get(f"/simulation/artifacts/{artifact_id}", headers=auth(viewer_user))
    assert r2.status_code == 200
    a = r2.json()
    assert a["artifact_id"] == artifact_id
    assert "curves" in a
    assert "time_s" in a["curves"]
    assert "speed_mps" in a["curves"]
