def test_export_csv(client, draft_snapshot, viewer_user):
    r1 = client.post(
        "/simulation/jobs",
        json={"snapshot_id": draft_snapshot.id},
        headers=auth(viewer_user),
    )
    assert r1.status_code == 200
    artifact_id = r1.json()["artifact_id"]

    r2 = client.get(f"/simulation/artifacts/{artifact_id}/export.csv", headers=auth(viewer_user))
    assert r2.status_code == 200
    assert "text/csv" in r2.headers.get("content-type", "")
    txt = r2.text
    assert txt.splitlines()[0].startswith("time_s,speed_mps,rpm,engine_temp_c,grip")
