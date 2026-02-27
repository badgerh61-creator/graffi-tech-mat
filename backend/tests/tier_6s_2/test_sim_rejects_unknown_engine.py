def test_sim_rejects_unknown_engine(client, draft_snapshot, viewer_user):
    r = client.post(
        "/simulation/jobs",
        json={"snapshot_id": draft_snapshot.id, "engine_version": "unknown-v9"},
        headers=auth(viewer_user),
    )
    assert r.status_code == 422
