def test_endurance_is_deterministic(client, draft_snapshot, viewer_user):
    payload = {
        "snapshot_id": draft_snapshot.id,
        "engine_version": "pseudo-endurance-v1",
        "scenario": {"duration_s": 5.0, "timestep_s": 1.0, "throttle": 0.7},
    }
    r1 = client.post("/simulation/jobs", json=payload, headers=auth(viewer_user))
    r2 = client.post("/simulation/jobs", json=payload, headers=auth(viewer_user))
    assert r1.status_code == 200 and r2.status_code == 200

    a1 = client.get(f"/simulation/artifacts/{r1.json()['artifact_id']}", headers=auth(viewer_user)).json()
    a2 = client.get(f"/simulation/artifacts/{r2.json()['artifact_id']}", headers=auth(viewer_user)).json()

    # Deterministic curves (exact match)
    assert a1["curves"]["engine_temp_c"] == a2["curves"]["engine_temp_c"]
    assert a1["curves"]["grip"] == a2["curves"]["grip"]
