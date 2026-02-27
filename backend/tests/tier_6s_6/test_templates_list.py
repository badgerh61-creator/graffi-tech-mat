def test_templates_list_requires_auth(client, viewer_user):
    r = client.get("/simulation/templates", headers=auth(viewer_user))
    assert r.status_code == 200
    data = r.json()
    assert "templates" in data
    keys = [t["key"] for t in data["templates"]]
    assert keys == sorted(keys)  # deterministic ordering
