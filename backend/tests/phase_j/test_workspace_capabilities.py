def test_workspace_includes_capabilities(client, project):
    data = client.get(f"/workspace/{project.id}").json()
    assert isinstance(data["capabilities"], dict)


def test_workspace_never_grants_write_capabilities(client, project):
    caps = client.get(f"/workspace/{project.id}").json()["capabilities"]
    assert caps.get("canSaveScene", False) is False

