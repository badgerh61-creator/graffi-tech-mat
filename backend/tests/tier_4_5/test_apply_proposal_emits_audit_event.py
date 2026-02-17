def test_apply_proposal_emits_audit_event(
    db,
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
        },
        headers=auth(locked_owner_user),
    )
    print("STATUS:", r.status_code)
    print("BODY:", r.text)
    assert r.status_code == 200

    new_id = r.json()["new_snapshot_id"]

    events = (
        db.query(AuditLog)
        .filter(AuditLog.action == "assistant.proposal.applied")
        .filter(AuditLog.resource_id == new_id)
        .all()
    )
    assert len(events) == 1

