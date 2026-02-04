def test_snapshots_are_ordered(
    client,
    project_with_snapshots,
    viewer_user,
):
    response = client.get(
        f"/warehouse/projects/{project_with_snapshots.id}/snapshots",
        headers=auth(viewer_user),
    )

    items = response.json()
    timestamps = [i["created_at"] for i in items]

    assert timestamps == sorted(timestamps)

