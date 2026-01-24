# backend/app/api/__init__.py

from . import (
    auth,
    users,
    job,
    models,
    assets,
    upload,
    presign,
    admin,
    audit,
    exports,
    organizations,
    projects,

    # 🔵 Phase 5.2 — Selection & Target Resolution
    snapshots_resolve_target,
)


