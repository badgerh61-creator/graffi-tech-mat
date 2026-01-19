def test_assets_are_ordered_by_created_at(
    client,
    workspace_with_assets_out_of_order,
    owner_user,
):
    project = workspace_with_assets_out_of_order["project"]
    response = client.get(
        f"/workspaces/{project['id']}",
        headers=auth(owner_user),
    )

    assets = response.json()["assets"]
    timestamps = [a["created_at"] for a in assets]

    assert timestamps == sorted(timestamps)

