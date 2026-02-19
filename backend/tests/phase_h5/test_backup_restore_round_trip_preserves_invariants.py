from pathlib import Path

from sqlalchemy import text

from app.services.backup_restore import create_backup, restore_backup


def _truncate_all(db):
    # Conservative: only tables we touch in restore.
    # Order matters: children first, parents last.
    for t in [
        "jobs",
        "assistant_proposals",
        "draft_locks",
        "audit_logs",
        "rendered_snapshots",
        "projects",
        "mutation_journal",
        "users",
    ]:
        db.execute(text(f"DELETE FROM {t}"))
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

    assert meta2.row_counts.get("rendered_snapshots", 0) == 1
    assert meta2.row_counts.get("mutation_journal", 0) == 1
    assert meta2.row_counts.get("jobs", 0) == 1

    # Verify Job compatibility preserved (DB column survives restore)
    row = db.execute(
        text("SELECT state, retry_count, max_retries FROM jobs LIMIT 1")
    ).fetchone()
    assert row is not None
    assert row[0] == "CREATED"
    assert row[1] == 0
    assert row[2] == 3

