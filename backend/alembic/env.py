# backend/alembic/env.py

from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context
import os
import sys

# --- Add backend path so Alembic can import "app" ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.abspath(os.path.join(BASE_DIR, "..")))

# --- Import Base and ALL models explicitly ---
from app.db.base import Base
from app.models.user import User
from app.models.asset import Asset
from app.models.model import ModelRecord
from app.models.patch_registry import PatchRegistry

# ✅ ADD: ensure all tables are present in metadata for migrations
# (Add more imports here as you add new models over time)
from app.models.job import Job  # Phase S/H compatibility
# from app.models.rendered_snapshot import RenderedSnapshot
# from app.models.audit_log import AuditLog
# from app.models.assistant_proposal import AssistantProposal
# etc...

# --- Alembic config ---
config = context.config

# ✅ MINIMAL ADD: prefer DATABASE_URL if provided at runtime
_db_url = os.getenv("DATABASE_URL")
if _db_url:
    config.set_main_option("sqlalchemy.url", _db_url)

# ✅ ADD: optional SQLite safety switch for migrations that need ALTER TABLE semantics
# (kept off by default; turn on by setting ALEMBIC_SQLITE_BATCH=1)
_SQLITE_BATCH = os.getenv("ALEMBIC_SQLITE_BATCH", "0") == "1"

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata


def run_migrations_offline():
    url = config.get_main_option("sqlalchemy.url")

    # ✅ ADD: compare_type helps detect type changes during autogenerate
    # ✅ ADD: render_as_batch optional for SQLite
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,                 # ✅ ADD
        render_as_batch=_SQLITE_BATCH,     # ✅ ADD (optional; env-controlled)
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        # ✅ ADD: compare_type helps detect type changes during autogenerate
        # ✅ ADD: render_as_batch optional for SQLite
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,                 # ✅ ADD
            render_as_batch=_SQLITE_BATCH,     # ✅ ADD (optional; env-controlled)
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()

