from app.models.rendered_snapshot import RenderedSnapshot as Snapshot

def test_apply_proposal_executes_tool_and_creates_child_snapshot(
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
    assert r.status_code == 200
    data = r.json()

    new_snapshot = db.query(Snapshot).get(data["new_snapshot_id"])
    assert new_snapshot is not None
    assert new_snapshot.parent_snapshot_id == assistant_proposal.snapshot_id
    assert new_snapshot.status == "draft"

