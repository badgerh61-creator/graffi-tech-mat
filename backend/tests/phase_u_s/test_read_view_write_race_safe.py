from app.services.kernel_test_facade import *
from sqlalchemy.orm import Session

def test_read_view_write_race_safe(
    db,
    draft_snapshot,
    owner_user,
    viewer_user,
):
    start_session(db=db, user=owner_user, project_id=draft_snapshot.project_id)
    start_session(db=db, user=viewer_user, project_id=draft_snapshot.project_id)

    acquire_draft_lock(db=db, snapshot=draft_snapshot, user=owner_user)
    open_read_view(db=db, snapshot=draft_snapshot, user=viewer_user)

    # 🔒 FLUSH VISIBILITY
    db.commit()
    db.expire_all()

    thread_db = Session(bind=db.get_bind())

    fresh_snapshot = (
        thread_db.query(type(draft_snapshot))
        .filter_by(id=draft_snapshot.id)
        .one()
    )

    new_snapshot = execute_tool(
        db=thread_db,
        user=owner_user,
        snapshot=fresh_snapshot,
        tool="scale",
        params={"factor": 1.1},
    )

    assert new_snapshot.parent_snapshot_id == draft_snapshot.id
    thread_db.close()

