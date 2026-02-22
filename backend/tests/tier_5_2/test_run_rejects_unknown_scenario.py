def test_run_rejects_unknown_scenario(client, draft_snapshot, editor_user):
    r = client.post(
        f"/snapshots/{draft_snapshot.id}/testing/run",
        headers=auth(editor_user),
        json={"scenario_id": "nope"},
    )
    assert r.status_code == 404
