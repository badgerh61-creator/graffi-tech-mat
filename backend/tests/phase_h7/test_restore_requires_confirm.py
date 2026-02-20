import os
import tempfile
import pytest

from app.services.backup_restore import restore_database


def test_restore_requires_confirm():
    database_url = os.getenv("DATABASE_URL") or "sqlite:///graffi.db"

    with tempfile.TemporaryDirectory() as td:
        src = os.path.join(td, "dummy.db")
        with open(src, "wb") as f:
            f.write(b"x")

        with pytest.raises(ValueError):
            restore_database(database_url=database_url, src_path=src, confirm="NO")

