def test_apply_proposal_requires_confirm_true(
    client,
    assistant_proposal,
    owner_user,
):
    r = client.post(
        "/assistant/proposals/apply",
        json={
            "proposal_id": assistant_proposal.id,
            "snapshot_id": assistant_proposal.snapshot_id,
            "confirm": False,
        },
        headers=auth(owner_user),
    )
    assert r.status_code == 409

