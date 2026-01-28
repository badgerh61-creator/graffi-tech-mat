from app.services.draft_lock_service import (
    acquire_draft_lock,
    release_draft_lock,
    get_draft_lock,
)


def test_draft_unlock_success(
    db,
    draft_snapshot,
    editor_user,
):
    acquire_draft_lock(
        db=db,
        snapshot=draft_snapshot,
        user=editor_user,
    )

    release_draft_lock(
        db=db,
        snapshot=draft_snapshot,
        user=editor_user,
    )

    assert get_draft_lock(db=db, snapshot=draft_snapshot) is None

