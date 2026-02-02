from app.services.kernel_test_facade import *

def test_ownership_handoff_race_atomic(
    db,
    draft_snapshot,
    user_a,
    user_b,
):
    acquire_draft_lock(db=db, snapshot=draft_snapshot, user=user_a)

    handoff_draft_ownership(
        db=db,
        snapshot=draft_snapshot,
        from_user=user_a,
        to_user=user_b,
    )

    assert is_draft_owner(db=db, snapshot=draft_snapshot, user=user_b)
    assert not is_draft_owner(db=db, snapshot=draft_snapshot, user=user_a)

