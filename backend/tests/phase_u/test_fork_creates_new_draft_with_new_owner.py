from app.services.snapshot_fork import fork_snapshot


def test_fork_creates_new_draft_with_new_owner(
    db,
    draft_snapshot,
    user_b,
):
    """
    Phase U invariant:

    Forking a draft snapshot:
    - creates a new draft
    - assigns ownership to the forking user
    - preserves parent linkage
    """

    fork = fork_snapshot(
        db=db,
        parent_snapshot=draft_snapshot,
        user=user_b,
        reason="ownership-handoff",
    )

    assert fork.id != draft_snapshot.id
    assert fork.parent_snapshot_id == draft_snapshot.id
    assert fork.created_by == user_b.id
    assert fork.status == "draft"

