def test_scenarios_list_returns_items(client, viewer_user):
    r = client.get("/testing/scenarios", headers=auth(viewer_user))
    assert r.status_code == 200
    data = r.json()
    assert isinstance(data, list)
    assert len(data) >= 1
    assert "id" in data[0]
    assert "category" in data[0]
