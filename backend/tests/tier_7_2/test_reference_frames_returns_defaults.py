def test_reference_frames_returns_defaults(client, draft_snapshot, viewer_user):
    r = client.get(
        f"/snapshots/{draft_snapshot.id}/reference-frames",
        headers=auth(viewer_user),
    )
    assert r.status_code == 200
    data = r.json()

    assert data["snapshot_id"] == draft_snapshot.id
    assert "axes" in data and "planes" in data and "defaults" in data
    assert isinstance(data["planes"], list)
    assert len(data["planes"]) >= 3
    assert data["defaults"]["active_plane_id"] in {p["id"] for p in data["planes"]}
