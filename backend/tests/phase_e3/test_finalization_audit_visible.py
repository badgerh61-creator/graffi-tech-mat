def test_finalization_audit_visible(
    client,
    completed_snapshot,
    editor_user,
):
    res = client.get(
        f"/audit?snapshot_id={completed_snapshot.id}",
        headers=auth(editor_user),
    )

    events = res.json()
    assert any(e["action"] == "snapshot.finalized" for e in events)

