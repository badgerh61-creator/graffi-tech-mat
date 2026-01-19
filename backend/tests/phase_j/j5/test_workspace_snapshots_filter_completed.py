def test_workspace_returns_only_completed_snapshots_by_default(
    client,
    workspace_with_mixed_snapshots,
    owner_user,
):
    project = workspace_with_mixed_snapshots["project"]
    response = client.get(
        f"/workspaces/{project['id']}",
        headers=auth(owner_user),
    )


    snapshots = response.json()["snapshots"]

    assert all(s["status"] == "completed" for s in snapshots)

