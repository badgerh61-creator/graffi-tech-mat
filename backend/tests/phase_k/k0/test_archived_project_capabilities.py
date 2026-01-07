def test_archived_project_has_no_write_capabilities(
    client,
    archived_project,
    owner_user,
):
    response = client.get(
        f"/workspaces/{archived_project.id}",
        headers=auth(owner_user),
    )

    caps = response.json()["capabilities"]

    assert all(value is False for value in caps.values())

