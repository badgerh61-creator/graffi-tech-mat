def test_compare_endpoint(client, draft_snapshot, viewer_user):
    rA = client.post(
        "/simulation/jobs",
        json={"snapshot_id": draft_snapshot.id, "scenario": {"throttle": 0.3}},
        headers=auth(viewer_user),
    )
    rB = client.post(
        "/simulation/jobs",
        json={"snapshot_id": draft_snapshot.id, "scenario": {"throttle": 0.8}},
        headers=auth(viewer_user),
    )
    assert rA.status_code == 200 and rB.status_code == 200
    a_id = rA.json()["artifact_id"]
    b_id = rB.json()["artifact_id"]

    r = client.post(
        "/simulation/compare",
        json={"a_artifact_id": a_id, "b_artifact_id": b_id},
        headers=auth(viewer_user),
    )
    assert r.status_code == 200
    out = r.json()
    assert out["a_artifact_id"] == a_id
    assert out["b_artifact_id"] == b_id
    assert "speed_avg_mps" in out["delta"]
