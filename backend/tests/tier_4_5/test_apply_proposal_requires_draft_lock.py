def test_apply_proposal_requires_draft_lock(
    client,
    assistant_proposal,
    editor_user_without_lock,
):
    r = client.post(
        "/assistant/proposals/apply",
        json={
            "proposal_id": assistant_proposal.id,
            "snapshot_id": assistant_proposal.snapshot_id,
            "confirm": True,
        },
        headers=auth(editor_user_without_lock),
    )
    assert r.status_code == 403

