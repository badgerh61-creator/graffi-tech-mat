def test_failed_snapshots_hidden_without_flag(
    client,
    workspace_with_failed_snapshot,
    owner_user,
):
    project = workspace_with_failed_snapshot["project"]

    response = client.get(
        f"/workspaces/{project['id']}",
        headers=auth(owner_user),
    )

    snapshots = response.json()["snapshots"]

    assert all(s["status"] == "completed" for s in snapshots)

