import subprocess


def test_alembic_upgrade_head_runs():
    r = subprocess.run(["alembic", "upgrade", "head"], capture_output=True, text=True)
    assert r.returncode == 0, r.stderr

