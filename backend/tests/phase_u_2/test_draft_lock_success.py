from app.services.draft_lock_service import acquire_draft_lock


def test_draft_lock_success(
    db,
    draft_snapshot,
    editor_user,
):
    lock = acquire_draft_lock(
        db=db,
        snapshot=draft_snapshot,
        user=editor_user,
    )

    assert lock.snapshot_id == draft_snapshot.id
    assert lock.user_id == editor_user.id

