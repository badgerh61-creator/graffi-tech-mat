def test_workspace_is_read_only(client, project):
    res = client.get(f"/workspace/{project.id}")
    assert res.status_code == 200
    assert "mutations" not in res.json()

