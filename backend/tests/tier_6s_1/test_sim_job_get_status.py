def test_sim_job_get_status(client, draft_snapshot, viewer_user):
    r1 = client.post("/simulation/jobs", json={"snapshot_id": draft_snapshot.id}, headers=auth(viewer_user))
    assert r1.status_code == 200
    job_id = r1.json()["job_id"]

    r2 = client.get(f"/simulation/jobs/{job_id}", headers=auth(viewer_user))
    assert r2.status_code == 200
    j = r2.json()
    assert j["job_id"] == job_id
    assert j["snapshot_id"] == draft_snapshot.id
