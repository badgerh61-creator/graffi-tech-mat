from app.services.kernel_test_facade import *
from sqlalchemy.orm import Session
import threading

def test_concurrent_write_attempts_single_writer(
    db,
    draft_snapshot,
    user_a,
    user_b,
):
    start_session(db=db, user=user_a, project_id=draft_snapshot.project_id)
    start_session(db=db, user=user_b, project_id=draft_snapshot.project_id)

    acquire_draft_lock(db=db, snapshot=draft_snapshot, user=user_a)

    # 🔒 MAKE STATE VISIBLE
    db.commit()
    db.expire_all()

    results = []

    def attempt_write(user):
        thread_db = Session(bind=db.get_bind())
        try:
            fresh_snapshot = (
                thread_db.query(type(draft_snapshot))
                .filter_by(id=draft_snapshot.id)
                .one()
            )

            execute_tool(
                db=thread_db,
                user=user,
                snapshot=fresh_snapshot,
                tool="translate",
                params={"x": 1},
            )
            results.append("success")
        except Exception:
            results.append("blocked")
        finally:
            thread_db.close()

    t1 = threading.Thread(target=attempt_write, args=(user_a,))
    t2 = threading.Thread(target=attempt_write, args=(user_b,))

    t1.start()
    t2.start()
    t1.join()
    t2.join()

    assert results.count("success") <= 1
    assert results.count("blocked") >= 1

