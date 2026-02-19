from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List

from sqlalchemy import text
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
        "version": "h5-v1",
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
) -> BackupMetadata:
    """
    Restore a backup into a DB.
    For ops-grade safety, default requires an empty target (require_empty=True).
    """
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(path)

    data = json.loads(p.read_text(encoding="utf-8"))
    if data.get("version") != "h5-v1":
        raise ValueError("Unsupported backup version")

    all_tables = list((data.get("tables") or {}).keys())
    tables = tables or all_tables

    # Safety: require empty tables (prevents accidental overwrite)
    if require_empty:
        for t in tables:
            res = db.execute(text(f"SELECT COUNT(*) FROM {t}"))
            count = int(res.scalar() or 0)
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

