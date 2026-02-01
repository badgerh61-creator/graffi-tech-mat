from app.kernel import acquire_draft_lock, release_draft_lock, handoff_draft_ownership
from app.services.presence_sessions import start_session

def test_handoff_enables_new_owner_execution(
    db,
    draft_snapshot,
    owner_user,
    target_user,
):
    acquire_draft_lock(db=db, snapshot=draft_snapshot, user=owner_user)

    mark_user_present(target_user)  # 🔑 REQUIRED BY CONTRACT

    handoff_draft_ownership(
        db=db,
        snapshot=draft_snapshot,
        from_user=owner_user,
        to_user=target_user,
    )

    # new owner can now act
    start_session(db=db, user=target_user, project_id=draft_snapshot.project_id)

    execute_tool(
        db=db,
        user=target_user,
        snapshot=draft_snapshot,
        tool="translate",
        params={"x": 1},
    )

