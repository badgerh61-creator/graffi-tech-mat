def test_apply_rejects_payload_hash_mismatch(
    client,
    assistant_proposal,
    locked_owner_user,
):
    r = client.post(
        "/assistant/proposals/apply",
        json={
            "proposal_id": assistant_proposal.id,
            "snapshot_id": assistant_proposal.snapshot_id,
            "confirm": True,
            "payload_hash": "deadbeef",  # wrong
        },
        headers=auth(locked_owner_user),
    )
    assert r.status_code == 409

