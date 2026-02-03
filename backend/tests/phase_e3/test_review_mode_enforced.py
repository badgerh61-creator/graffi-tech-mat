def test_review_mode_enforced(
    client,
    completed_snapshot,
    viewer_user,
):
    res = client.get(
        f"/studio/context?snapshot_id={completed_snapshot.id}",
        headers=auth(viewer_user),
    )

    ctx = res.json()
    assert ctx["mode"] == "read-only"
    assert ctx["station"] == "review"

