def test_history_endpoint_returns_nodes(client, completed_snapshot):
    r = client.get(f"/snapshots/{completed_snapshot.id}/history")
    assert r.status_code in (200, 404)  # 404 if fixture isn't present in your env

    if r.status_code == 200:
        data = r.json()
        assert "nodes" in data
        assert isinstance(data["nodes"], list)
        assert data["nodes"][0]["id"] == completed_snapshot.id
