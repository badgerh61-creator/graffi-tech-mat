from sqlalchemy import text
import pytest

from app.services.backup_restore import create_backup, restore_backup


def test_restore_requires_empty_by_default(db, tmp_path):
    unique_email = f"restore_nonempty_{tmp_path.name}@test.local"

    db.execute(
        text(
            """
            INSERT INTO users (email, hashed_password, role, is_active, is_admin, can_tune)
            VALUES (:email, 'x', 'admin', 1, 1, 1)
            """
        ),
        {"email": unique_email},
    )
    db.commit()

    path = str(tmp_path / "b.json")
    create_backup(db=db, path=path)

    # Do NOT empty DB, restore should fail by default
    with pytest.raises(ValueError):
        restore_backup(db=db, path=path, require_empty=True)

