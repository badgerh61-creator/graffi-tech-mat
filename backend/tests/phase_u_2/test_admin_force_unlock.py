from app.services.draft_lock_service import (
    acquire_draft_lock,
    release_draft_lock,
    get_draft_lock,
)


def test_admin_force_unlock(
    db,
    draft_snapshot,
    editor_user,
    admin_user,
):
    acquire_draft_lock(
        db=db,
        snapshot=draft_snapshot,
        user=editor_user,
    )

    release_draft_lock(
        db=db,
        snapshot=draft_snapshot,
        user=admin_user,
        force=True,
    )

    assert get_draft_lock(db=db, snapshot=draft_snapshot) is None

