def test_draft_autosave_updates_state(
    client,
    draft_snapshot,
    editor_user,
):
    res = client.patch(
        f"/snapshots/{draft_snapshot.id}/autosave",
        json={"scene_state_hash": "new_hash"},
        headers=auth(editor_user),
    )

    assert res.status_code == 200
    assert res.json()["scene_state_hash"] == "new_hash"

