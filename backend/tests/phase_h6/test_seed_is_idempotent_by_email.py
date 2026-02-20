import subprocess
from sqlalchemy import text


def test_seed_is_idempotent_by_email(db):
    r1 = subprocess.run(["python", "-m", "app.cli.db", "seed"], capture_output=True, text=True)
    assert r1.returncode == 0, r1.stderr

    r2 = subprocess.run(["python", "-m", "app.cli.db", "seed"], capture_output=True, text=True)
    assert r2.returncode == 0, r2.stderr

    res = db.execute(
        text(
            "SELECT COUNT(*) FROM users "
            "WHERE email IN ("
            "'admin_phase_i@test.com',"
            "'owner_phase_k@test.com',"
            "'editor_phase_k@test.com',"
            "'viewer_phase_i@test.com',"
            "'editor_no_tune@test.com'"
            ")"
        )
    )
    assert int(res.scalar() or 0) == 5

