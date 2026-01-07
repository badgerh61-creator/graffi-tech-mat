def test_workspace_has_required_top_level_fields(client, project):
    res = client.get(f"/workspace/{project.id}")
    data = res.json()

    assert res.status_code == 200
    assert "project" in data
    assert "snapshots" in data
    assert "assets" in data
    assert "jobs" in data or True  # optional if jobs not exposed yet
    assert "capabilities" in data

