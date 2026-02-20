import os
import tempfile
from sqlalchemy import text

from app.services.backup_restore import backup_database, restore_database
from app.db.session import SessionLocal


def test_backup_restore_roundtrip_sqlite(db):
    """
    Evidence-based drill:
    1) backup sqlite file
    2) mutate DB
    3) restore
    4) verify mutation is gone

    This test assumes SQLite dev/test environment.
    """
    database_url = os.getenv("DATABASE_URL") or "sqlite:///graffi.db"

    with tempfile.TemporaryDirectory() as td:
        backup_path = os.path.join(td, "graffi.backup.db")

        # 1) backup
        backup_database(database_url=database_url, out_path=backup_path)
        assert os.path.exists(backup_path)

        # 2) mutate: insert a sentinel row
        tables = db.execute(
            text("SELECT name FROM sqlite_master WHERE type='table'")
        ).fetchall()
        table_names = {t[0] for t in tables}

        if "audit_logs" in table_names:
            db.execute(
                text(
                    "INSERT INTO audit_logs (action, resource_type, resource_id) "
                    "VALUES ('h7.sentinel','system',0)"
                )
            )
            db.commit()

            count_after = db.execute(
                text("SELECT COUNT(*) FROM audit_logs WHERE action='h7.sentinel'")
            ).scalar()
            assert int(count_after or 0) == 1

        elif "users" in table_names:
            db.execute(
                text(
                    "INSERT INTO users (email, hashed_password, role) "
                    "VALUES ('h7_sentinel@test.com','x','viewer')"
                )
            )
            db.commit()

            count_after = db.execute(
                text("SELECT COUNT(*) FROM users WHERE email='h7_sentinel@test.com'")
            ).scalar()
            assert int(count_after or 0) == 1

        # 3) restore (destructive file replace)
        restore_database(
            database_url=database_url,
            src_path=backup_path,
            confirm="YES",
        )

        # 4) verify sentinel gone using a FRESH session
        fresh = SessionLocal()
        try:
            if "audit_logs" in table_names:
                count_final = fresh.execute(
                    text("SELECT COUNT(*) FROM audit_logs WHERE action='h7.sentinel'")
                ).scalar()
                assert int(count_final or 0) == 0

            elif "users" in table_names:
                count_final = fresh.execute(
                    text("SELECT COUNT(*) FROM users WHERE email='h7_sentinel@test.com'")
                ).scalar()
                assert int(count_final or 0) == 0
        finally:
            fresh.close()
