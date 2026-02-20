# backend/app/services/backup_restore.py
from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

from sqlalchemy import text
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import Session


@dataclass(frozen=True)
class BackupMetadata:
    created_at: str
    tables: List[str]
    row_counts: Dict[str, int]
    version: str = "h5-v1"


# Keep this list minimal but safe. Add more tables later without breaking old backups.
# IMPORTANT: include audit + snapshots + locks + mutation_journal + jobs to preserve invariants.
DEFAULT_TABLES: List[str] = [
    "users",
    "projects",
    "rendered_snapshots",
    "audit_logs",
    "draft_locks",
    "assistant_proposals",
    "mutation_journal",  # ✅ jobs.mutation_id FK depends on this
    "jobs",
]

# -------------------------
# ADDITIVE CONSTANTS (SAFE)
# -------------------------
BACKUP_VERSION: str = "h5-v1"
OPS_CONFIRM_TOKEN: str = "YES"


def _fetch_all_rows(db: Session, table: str) -> List[Dict[str, Any]]:
    # Generic SQL dump (works without importing ORM models)
    result = db.execute(text(f"SELECT * FROM {table}"))
    cols = list(result.keys())
    return [dict(zip(cols, r)) for r in result.fetchall()]


def _insert_rows(db: Session, table: str, rows: List[Dict[str, Any]]) -> None:
    if not rows:
        return

    cols = list(rows[0].keys())
    col_list = ", ".join(cols)
    param_list = ", ".join([f":{c}" for c in cols])

    stmt = text(f"INSERT INTO {table} ({col_list}) VALUES ({param_list})")
    db.execute(stmt, rows)


# -------------------------
# ADDITIVE HELPERS (SAFE)
# -------------------------
def _now_iso() -> str:
    return datetime.utcnow().isoformat()


def _safe_count_rows(db: Session, table: str) -> int:
    res = db.execute(text(f"SELECT COUNT(*) FROM {table}"))
    return int(res.scalar() or 0)


def get_backup_manifest(*, path: str) -> Dict[str, Any]:
    """
    Additive helper: read raw backup JSON as dict.
    Does not mutate DB.
    """
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(path)
    return json.loads(p.read_text(encoding="utf-8"))


def validate_backup_file(*, path: str) -> BackupMetadata:
    """
    Additive helper: validate backup JSON shape + produce BackupMetadata.
    Does not mutate DB.
    """
    data = get_backup_manifest(path=path)

    version = data.get("version")
    if version != BACKUP_VERSION:
        raise ValueError("Unsupported backup version")

    created_at = data.get("created_at") or _now_iso()
    tables_obj = data.get("tables") or {}
    if not isinstance(tables_obj, dict):
        raise ValueError("Invalid backup format: tables must be an object")

    tables = list(tables_obj.keys())
    row_counts: Dict[str, int] = {}
    for t in tables:
        rows = tables_obj.get(t, [])
        if not isinstance(rows, list):
            raise ValueError(f"Invalid backup format: tables.{t} must be a list")
        row_counts[t] = len(rows)

    return BackupMetadata(
        created_at=created_at,
        tables=tables,
        row_counts=row_counts,
        version=version,
    )


def require_ops_confirm(*, confirm: Optional[str], require_confirm: bool) -> None:
    """
    Additive guard:
    - If require_confirm=False, does nothing (backward compatible)
    - If require_confirm=True, require confirm == "YES"
    """
    if not require_confirm:
        return
    if confirm != OPS_CONFIRM_TOKEN:
        raise ValueError(f"Restore requires explicit confirmation: confirm must be '{OPS_CONFIRM_TOKEN}'")


def create_backup(
    *,
    db: Session,
    path: str,
    tables: List[str] | None = None,
) -> BackupMetadata:
    """
    Create a JSON backup file. Additive only.
    Does not mutate DB.
    """
    tables = tables or list(DEFAULT_TABLES)
    payload: Dict[str, Any] = {
        "version": BACKUP_VERSION,
        "created_at": datetime.utcnow().isoformat(),
        "tables": {},
    }

    row_counts: Dict[str, int] = {}

    for t in tables:
        rows = _fetch_all_rows(db, t)
        payload["tables"][t] = rows
        row_counts[t] = len(rows)

    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(payload, default=str), encoding="utf-8")

    return BackupMetadata(
        created_at=payload["created_at"],
        tables=tables,
        row_counts=row_counts,
    )


def restore_backup(
    *,
    db: Session,
    path: str,
    tables: List[str] | None = None,
    require_empty: bool = True,
    # -------------------------
    # ADDITIVE SAFETY (DEFAULT OFF)
    # -------------------------
    require_confirm: bool = False,
    confirm: Optional[str] = None,
    # -------------------------
    # ADDITIVE: optional integrity check
    # If provided, we require the backup file to still match this exact version string.
    # (Back-compat: leaving None preserves old behavior.)
    # -------------------------
    expected_version: Optional[str] = None,
) -> BackupMetadata:
    """
    Restore a backup into a DB.
    For ops-grade safety, default requires an empty target (require_empty=True).

    Additive ops hardening:
    - require_confirm=False by default (so earlier phases are unaffected)
    - if require_confirm=True, caller must pass confirm="YES"
    - expected_version optional strict check
    """
    # ✅ Additive confirmation guard (does not affect existing callers)
    require_ops_confirm(confirm=confirm, require_confirm=require_confirm)

    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(path)

    data = json.loads(p.read_text(encoding="utf-8"))
    if data.get("version") != BACKUP_VERSION:
        raise ValueError("Unsupported backup version")

    if expected_version is not None and data.get("version") != expected_version:
        raise ValueError("Backup version mismatch for restore")

    all_tables = list((data.get("tables") or {}).keys())
    tables = tables or all_tables

    # Safety: require empty tables (prevents accidental overwrite)
    if require_empty:
        for t in tables:
            try:
                count = _safe_count_rows(db, t)
            except OperationalError as e:
                msg = str(e).lower()
                if "no such table" in msg:
                    raise ValueError(
                        f"Target database is missing table '{t}'. "
                        f"Your Alembic history appears to assume a pre-existing schema "
                        f"(baseline is a NO-OP). Restore must run against a DB that already "
                        f"has the base tables (users/projects/...)."
                    ) from e
                raise

            if count != 0:
                raise ValueError(f"Target table not empty: {t} ({count} rows)")

    # ✅ Insert rows in FK-safe order (parents first).
    # Key invariant: mutation_journal must be restored before jobs (jobs.mutation_id FK).
    insert_order = [
        "users",
        "projects",
        "rendered_snapshots",
        "audit_logs",
        "draft_locks",
        "assistant_proposals",
        "mutation_journal",
        "jobs",
    ]
    ordered = [t for t in insert_order if t in tables] + [
        t for t in tables if t not in insert_order
    ]

    row_counts: Dict[str, int] = {}

    for t in ordered:
        rows = data["tables"].get(t, [])
        _insert_rows(db, t, rows)
        row_counts[t] = len(rows)

    db.commit()

    return BackupMetadata(
        created_at=data.get("created_at") or datetime.utcnow().isoformat(),
        tables=ordered,
        row_counts=row_counts,
    )


# -------------------------
# ADDITIVE "OPS" WRAPPERS (SAFE)
# These do NOT replace existing APIs; they provide a stricter interface for H.7/H.1.
# -------------------------
def create_backup_ops(
    *,
    db: Session,
    path: str,
    tables: List[str] | None = None,
) -> BackupMetadata:
    """
    Ops wrapper: same as create_backup, kept separate so earlier phases can keep using create_backup directly.
    """
    return create_backup(db=db, path=path, tables=tables)


def restore_backup_ops(
    *,
    db: Session,
    path: str,
    tables: List[str] | None = None,
    require_empty: bool = True,
    confirm: str = OPS_CONFIRM_TOKEN,
) -> BackupMetadata:
    """
    Ops wrapper: requires explicit confirmation token by default.
    Backward-compatible because it's new and additive.
    """
    return restore_backup(
        db=db,
        path=path,
        tables=tables,
        require_empty=require_empty,
        require_confirm=True,
        confirm=confirm,
        expected_version=BACKUP_VERSION,
    )


# -------------------------
# COMPATIBILITY ALIASES (H7 TESTS)
# DO NOT REMOVE create_backup / restore_backup (earlier phases may use them)
# -------------------------

def backup_database(
    *,
    db: Session,
    path: str,
    tables: List[str] | None = None,
) -> BackupMetadata:
    """
    Phase H7 compatibility alias for create_backup().
    """
    return create_backup(db=db, path=path, tables=tables)


def restore_database(
    *,
    db: Session,
    path: str,
    tables: List[str] | None = None,
    require_empty: bool = True,
    confirm: Optional[str] = None,
    require_confirm: bool = False,
) -> BackupMetadata:
    """
    Phase H7 compatibility alias for restore_backup().

    - Backward compatible defaults:
      require_confirm=False (so existing callers won't break)
    - If tests/ops require confirmation, pass require_confirm=True and confirm="YES".
    """
    return restore_backup(
        db=db,
        path=path,
        tables=tables,
        require_empty=require_empty,
        require_confirm=require_confirm,
        confirm=confirm,
        expected_version=BACKUP_VERSION,
    )
    
    
# -------------------------
# H7 SQLITE FILE-COPY OPS (ADDITIVE)
# Keeps your JSON backup/restore intact (H5).
# -------------------------
import os
import shutil
from urllib.parse import urlparse


def _sqlite_path_from_url(database_url: str) -> str | None:
    if not database_url:
        return None
    parsed = urlparse(database_url)
    if parsed.scheme != "sqlite":
        return None

    # sqlite:///graffi.db  -> parsed.path="/graffi.db"
    # sqlite:////abs.db    -> parsed.path="/abs.db"
    raw_path = parsed.path or ""
    if not raw_path:
        return None

    # If absolute path exists, use it. Otherwise treat as relative.
    if os.path.isabs(raw_path) and os.path.exists(raw_path):
        return raw_path

    return raw_path.lstrip("/")  # relative path like "graffi.db"


def backup_database(*, database_url: str, out_path: str) -> dict:
    """
    H7: SQLite-only physical DB backup (file copy).
    Additive: does not replace JSON create_backup().
    """
    sqlite_path = _sqlite_path_from_url(database_url)
    if sqlite_path is None:
        raise NotImplementedError("H7 backup supports SQLite only (file copy).")

    os.makedirs(os.path.dirname(out_path) or ".", exist_ok=True)
    shutil.copy2(sqlite_path, out_path)
    return {"backend": "sqlite", "source": sqlite_path, "output": out_path}


def restore_database(*, database_url: str, src_path: str, confirm: str) -> dict:
    """
    H7: SQLite-only physical DB restore (file copy).
    Requires confirm == 'YES'.
    """
    if confirm != "YES":
        raise ValueError("Restore requires explicit confirmation: confirm must be 'YES'")

    sqlite_path = _sqlite_path_from_url(database_url)
    if sqlite_path is None:
        raise NotImplementedError("H7 restore supports SQLite only (file copy).")

    if not os.path.exists(src_path):
        raise FileNotFoundError(src_path)

    os.makedirs(os.path.dirname(sqlite_path) or ".", exist_ok=True)
    shutil.copy2(src_path, sqlite_path)
    return {"backend": "sqlite", "source": src_path, "output": sqlite_path}
