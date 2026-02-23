def test_reference_frames_deterministic(client, draft_snapshot, viewer_user):
    r1 = client.get(
        f"/snapshots/{draft_snapshot.id}/reference-frames",
        headers=auth(viewer_user),
    )
    r2 = client.get(
        f"/snapshots/{draft_snapshot.id}/reference-frames",
        headers=auth(viewer_user),
    )
    assert r1.status_code == 200
    assert r2.status_code == 200
    assert r1.json() == r2.json()
