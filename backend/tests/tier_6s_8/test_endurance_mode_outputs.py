def test_endurance_engine_outputs_curves(client, draft_snapshot, viewer_user):
    r = client.post(
        "/simulation/jobs",
        json={
            "snapshot_id": draft_snapshot.id,
            "engine_version": "pseudo-endurance-v1",
            "scenario": {"duration_s": 5.0, "timestep_s": 1.0, "throttle": 0.7},
        },
        headers=auth(viewer_user),
    )
    assert r.status_code == 200
    artifact_id = r.json()["artifact_id"]

    a = client.get(f"/simulation/artifacts/{artifact_id}", headers=auth(viewer_user))
    assert a.status_code == 200
    out = a.json()
    assert out["engine_version"] == "pseudo-endurance-v1"
    assert "curves" in out
    assert "engine_temp_c" in out["curves"]
    assert out.get("meta", {}).get("mode") == "endurance"
