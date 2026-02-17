def test_apply_proposal_rejects_tool_not_registered(
    client,
    unregistered_tool_proposal,
    locked_owner_user,
):
    r = client.post(
        "/assistant/proposals/apply",
        json={
            "proposal_id": unregistered_tool_proposal.id,
            "snapshot_id": unregistered_tool_proposal.snapshot_id,
            "confirm": True,
        },
        headers=auth(locked_owner_user),
    )
    assert r.status_code == 422

