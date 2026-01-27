from app.services.snapshot_fork import fork_snapshot

def test_fork_creates_new_draft_with_new_owner(
    db,
    completed_snapshot,
    user_b,
):
    fork = fork_snapshot(
        db=db,
        snapshot=completed_snapshot,
        user=user_b,
    )

    assert fork.id != completed_snapshot.id
    assert fork.parent_snapshot_id == completed_snapshot.id
    assert fork.owner_user_id == user_b.id
    assert fork.status == "draft"

