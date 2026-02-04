def test_warehouse_does_not_create_drafts(
    db,
    client,
    project_with_snapshots,
    viewer_user,
):
    before = count_snapshots(db)

    client.get(
        f"/warehouse/projects/{project_with_snapshots.id}",
        headers=auth(viewer_user),
    )

    after = count_snapshots(db)
    assert before == after

