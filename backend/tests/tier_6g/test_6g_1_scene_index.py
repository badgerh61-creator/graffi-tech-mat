def test_scene_index_returns_objects(client, completed_snapshot):
    resp = client.get(
        f"/projects/{completed_snapshot.project_id}/snapshots/{completed_snapshot.id}/scene"
    )
    assert resp.status_code == 200

    data = resp.json()
    assert data["snapshot_id"] == completed_snapshot.id
    assert isinstance(data["objects"], list)
    assert len(data["objects"]) >= 1

    # Validate the first object shape (stub guarantees >= 1)
    obj = data["objects"][0]
    assert isinstance(obj, dict)

    assert obj.get("id")
    assert obj.get("kind")
    assert "name" in obj
    assert "asset_ref" in obj

    t = obj.get("transform")
    assert isinstance(t, dict)
    assert set(t.keys()) >= {"position", "rotation", "scale"}

    for k in ("position", "rotation", "scale"):
        v = t[k]
        assert isinstance(v, dict)
        assert set(v.keys()) >= {"x", "y", "z"}


def test_scene_index_404_when_snapshot_missing(client, project):
    resp = client.get(f"/projects/{project.id}/snapshots/999999999/scene")
    assert resp.status_code == 404
