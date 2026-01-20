def test_autosave_rejected_for_completed(
    client,
    completed_snapshot,
    editor_user,
):
    res = client.patch(
        f"/snapshots/{completed_snapshot.id}/autosave",
        json={"scene_state_hash": "bad"},
        headers=auth(editor_user),
    )

    assert res.status_code == 409

