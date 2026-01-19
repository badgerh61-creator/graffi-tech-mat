def test_snapshots_are_ordered_by_created_at(
    client,
    workspace_with_multiple_snapshots,
    owner_user,
):
    project = workspace_with_multiple_snapshots["project"]
    response = client.get(
        f"/workspaces/{project['id']}",
        headers=auth(owner_user),
    )


    snapshots = response.json()["snapshots"]
    times = [s["created_at"] for s in snapshots]

    assert times == sorted(times)

