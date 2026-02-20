# tests/phase_h5/test_backup_restore_round_trip_preserves_invariants.py

from __future__ import annotations

from pathlib import Path

import pytest
from sqlalchemy import text

from app.services.backup_restore import create_backup, restore_backup


def _truncate_all(db) -> None:
    """
    Wipe only the tables involved in backup/restore tests.

    SQLite will enforce FK constraints on DELETE, so we:
    - Disable FK checks during the wipe (SQLite only)
    - Delete in FK-safe order (children first) as an extra safety net
    """
    dialect = getattr(getattr(db, "bind", None), "dialect", None)
    dialect_name = getattr(dialect, "name", "")

    if dialect_name == "sqlite":
        db.execute(text("PRAGMA foreign_keys=OFF"))

    # FK-safe order (children -> parents)
    ordered = [
        "jobs",
        "mutation_journal",
        "assistant_proposals",
        "draft_locks",
        "audit_logs",
        "rendered_snapshots",
        "projects",
        "users",
    ]

    for t in ordered:
        db.execute(text(f"DELETE FROM {t}"))

    if dialect_name == "sqlite":
        db.execute(text("PRAGMA foreign_keys=ON"))

    db.commit()


def test_backup_restore_round_trip_preserves_invariants(db, tmp_path):
    # Seed minimal rows using raw SQL, but MUST satisfy NOT NULL + FK constraints.
    # Do NOT hardcode ids/emails: fixture DB may already contain rows.

    unique_email = f"backup_restore_{tmp_path.name}@test.local"

    # USERS (schema has NOT NULL flags)
    db.execute(
        text(
            """
            INSERT INTO users (email, hashed_password, role, is_active, is_admin, can_tune)
            VALUES (:email, 'x', 'admin', 1, 1, 1)
            """
        ),
        {"email": unique_email},
    )
    user_id = int(db.execute(text("SELECT last_insert_rowid()")).scalar())

    # PROJECTS
    db.execute(
        text(
            """
            INSERT INTO projects (name, owner_id)
            VALUES ('P1', :owner_id)
            """
        ),
        {"owner_id": user_id},
    )
    project_id = int(db.execute(text("SELECT last_insert_rowid()")).scalar())

    # SNAPSHOTS (schema has NOT NULL fields like is_corrupted, created_by)
    db.execute(
        text(
            """
            INSERT INTO rendered_snapshots
              (project_id, status, scene_state_hash, render_profile, engine_version, is_corrupted, created_by)
            VALUES
              (:project_id, 'completed', '__completed__', 'default', 'test-engine', 0, :created_by)
            """
        ),
        {"project_id": project_id, "created_by": user_id},
    )
    snapshot_id = int(db.execute(text("SELECT last_insert_rowid()")).scalar())

    # AUDIT LOGS
    db.execute(
        text(
            """
            INSERT INTO audit_logs (user_id, action, resource_type, resource_id)
            VALUES (:user_id, 'snapshot.finalized', 'snapshot', :snapshot_id)
            """
        ),
        {"user_id": user_id, "snapshot_id": snapshot_id},
    )

    # MUTATION JOURNAL (jobs.mutation_id FK -> mutation_journal.id)
    db.execute(
        text(
            """
            INSERT INTO mutation_journal
              (intent_type, target_type, target_id, before_state, after_state, issued_by_user_id, reason)
            VALUES
              ('BackupRestoreTest', 'snapshot', :target_id, :before_state, :after_state, :issued_by, 'test seed')
            """
        ),
        {
            "target_id": snapshot_id,
            "before_state": "{}",
            "after_state": "{}",
            "issued_by": user_id,
        },
    )
    mutation_id = int(db.execute(text("SELECT last_insert_rowid()")).scalar())

    # JOBS (must reference valid mutation_id)
    db.execute(
        text(
            """
            INSERT INTO jobs (mutation_id, job_type, target_type, target_id, state, retry_count, max_retries)
            VALUES (:mutation_id, 'export', 'snapshot', :snapshot_id, 'CREATED', 0, 3)
            """
        ),
        {"mutation_id": mutation_id, "snapshot_id": snapshot_id},
    )
    db.commit()

    # BACKUP
    backup_path = str(tmp_path / "backup.json")
    meta1 = create_backup(db=db, path=backup_path)
    assert Path(backup_path).exists()
    assert meta1.row_counts.get("users", 0) >= 1

    # WIPE + RESTORE
    _truncate_all(db)

    meta2 = restore_backup(db=db, path=backup_path, require_empty=True)
    assert meta2.row_counts["users"] >= 1
    assert meta2.row_counts["projects"] >= 1
    assert meta2.row_counts["rendered_snapshots"] >= 1
    assert meta2.row_counts["audit_logs"] >= 1
    assert meta2.row_counts["mutation_journal"] >= 1
    assert meta2.row_counts["jobs"] >= 1


def test_backup_restore_requires_empty_by_default(db, tmp_path):
    # Create a backup from current DB
    backup_path = str(tmp_path / "backup.json")
    create_backup(db=db, path=backup_path)

    # Attempt restore into non-empty DB should fail
    with pytest.raises(ValueError) as e:
        restore_backup(db=db, path=backup_path, require_empty=True)

    assert "Target table not empty" in str(e.value)

