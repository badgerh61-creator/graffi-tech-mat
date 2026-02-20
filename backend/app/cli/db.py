from __future__ import annotations

import argparse
import subprocess
from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app import crud

DEFAULT_SEED_USERS = [
    ("admin_phase_i@test.com", "admin123", "admin"),
    ("owner_phase_k@test.com", "owner123", "owner"),
    ("editor_phase_k@test.com", "editor123", "editor"),
    ("viewer_phase_i@test.com", "viewer123", "viewer"),
    ("editor_no_tune@test.com", "editor123", "editor"),
]


def _run_alembic(args: list[str]) -> int:
    # Keep it external so we don't entangle phases.
    return subprocess.call(["alembic", *args])


def cmd_upgrade() -> int:
    return _run_alembic(["upgrade", "head"])


def _seed_user(db: Session, email: str, password: str, role: str) -> None:
    """
    Idempotent seed by email.
    IMPORTANT: uses existing CRUD entrypoints; does not rename anything.

    Strategy:
    1) Use crud.get_user_by_email (you already have this)
    2) Try common creator functions
    3) Fallback to direct ORM insert using existing password hashing helper
    """
    existing = crud.get_user_by_email(db, email)
    if existing:
        return

    # 1) If repo exposes a creator, use it
    if hasattr(crud, "create_user"):
        crud.create_user(db, {"email": email, "password": password, "role": role})
        return

    # Some repos use different names/signatures
    if hasattr(crud, "create_user_with_password"):
        crud.create_user_with_password(db, email=email, password=password, role=role)
        return

    # 2) Fallback: create User row directly (seed path only)
    from app.models.user import User

    # Try to locate a password-hash helper (common module names)
    hash_fn = None
    candidates = [
        ("app.core.security", "get_password_hash"),
        ("app.core.security", "hash_password"),
        ("app.services.security", "get_password_hash"),
        ("app.services.security", "hash_password"),
        ("app.auth.security", "get_password_hash"),
        ("app.auth.security", "hash_password"),
    ]
    for mod, fn in candidates:
        try:
            m = __import__(mod, fromlist=[fn])
            hash_fn = getattr(m, fn)
            break
        except Exception:
            continue

    if hash_fn is None:
        raise NotImplementedError(
            "Seed fallback needs a password hash function. "
            "Expose one as app.core.security.get_password_hash (recommended), "
            "or add crud.create_user."
        )

    hashed = hash_fn(password)

    u = User(email=email)

    # role field (common)
    if hasattr(u, "role"):
        setattr(u, "role", role)

    # password hash field (common)
    if hasattr(u, "hashed_password"):
        setattr(u, "hashed_password", hashed)
    elif hasattr(u, "password_hash"):
        setattr(u, "password_hash", hashed)
    else:
        raise NotImplementedError(
            "Seed fallback cannot set password: User model missing "
            "'hashed_password' or 'password_hash'. Add crud.create_user instead."
        )

    db.add(u)
    # NOTE: commit happens in cmd_seed()


def cmd_seed() -> int:
    db = SessionLocal()
    try:
        for email, pw, role in DEFAULT_SEED_USERS:
            _seed_user(db, email, pw, role)
        db.commit()
        return 0
    finally:
        db.close()


def main() -> None:
    p = argparse.ArgumentParser(prog="gtm-db")
    sub = p.add_subparsers(dest="cmd", required=True)

    sub.add_parser("upgrade")
    sub.add_parser("seed")

    args = p.parse_args()
    if args.cmd == "upgrade":
        raise SystemExit(cmd_upgrade())
    if args.cmd == "seed":
        raise SystemExit(cmd_seed())


if __name__ == "__main__":
    main()

