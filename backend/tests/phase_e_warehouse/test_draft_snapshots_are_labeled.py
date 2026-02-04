def test_draft_snapshots_are_labeled(
    client,
    draft_snapshot,
    viewer_user,
):
    response = client.get(
        f"/warehouse/projects/{draft_snapshot.project_id}/snapshots",
        headers=auth(viewer_user),
    )

    items = response.json()
    draft = next(i for i in items if i["snapshot_id"] == draft_snapshot.id)

    assert draft["status"] == "draft"

