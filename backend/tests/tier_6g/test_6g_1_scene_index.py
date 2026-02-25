def test_scene_index_returns_objects(client, completed_snapshot):
    # completed_snapshot should include .id and .project_id from your fixtures
    resp = client.get(f"/projects/{completed_snapshot.project_id}/snapshots/{completed_snapshot.id}/scene")
    assert resp.status_code == 200

    data = resp.json()
    assert data["snapshot_id"] == completed_snapshot.id
    assert isinstance(data["objects"], list)
    assert len(data["objects"]) >= 1

    obj = data["objects"][0]
    assert "id" in obj
    assert "kind" in obj
    assert "name" in obj
    assert "asset_ref" in obj
    assert "transform" in obj
    assert "position" in obj["transform"]
    assert "rotation" in obj["transform"]
    assert "scale" in obj["transform"]


def test_scene_index_404_when_snapshot_missing(client, project):
    resp = client.get(f"/projects/{project.id}/snapshots/999999999/scene")
    assert resp.status_code == 404
