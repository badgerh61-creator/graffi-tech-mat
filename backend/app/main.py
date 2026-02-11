# backend/app/main.py

from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import validate_settings
from app.db.base import Base
from app.db.session import engine

# ===== ROUTER IMPORTS =====
from app.api.auth import router as auth_router
from app.api.users import router as users_router
from app.api.projects import router as projects_router
from app.api.workspace import router as workspace_router
from app.api.job import router as jobs_router
from app.api.models import router as models_router
from app.api.assets import router as assets_router
from app.api.upload import router as upload_router
from app.api.presign import router as presign_router
from app.api.admin import router as admin_router
from app.api.audit import router as audit_router
from app.api.exports import router as exports_router
from app.api.distributions import router as distributions_router
from app.api.organizations import router as organizations_router
from app.api.scenes import router as scenes_router
from app.api.signed_urls import router as signed_url_router

# 🔑 SNAPSHOT ROUTERS (FIXED — NO SHADOWING)
from app.api.mutations.snapshots import router as snapshot_mutations_router
from app.api.snapshot_mutations import router as snapshot_mutations_legacy_router
from app.api.snapshots_legacy import router as snapshots_legacy_router
from app.api.snapshots import router as snapshots_router

from app.api.snapshots_transform import router as snapshots_transform_router
from app.api.snapshots_resolve_target import router as resolve_target_router
from app.api.snapshots_validate_transform import router as snapshots_validate_transform_router

from app.api.mutations import (
    router as phase_i_mutations_router,
    public_router,
)

from app.api.mutations.decor.exterior import router as decor_exterior_router
from app.api.mutations.tuning.router import router as tuning_router
from app.api.mutations.body.router import router as body_router

from app.api.snapshots_undo_redo import router as snapshots_undo_redo_router

# Studio (Phase E)
from app.api.studio_state import router as studio_state_router
from app.api.studio_tools import router as studio_tools_router
from app.api.studio_flow import router as studio_flow_router
from app.api.studio_snapshot_state import router as studio_snapshot_state_router
from app.api.studio_audit import router as studio_audit_router

from app.api.warehouse import router as warehouse_router
from app.api.exports_images import router as exports_images_router
from app.api.dashboard import router as dashboard_router
from app.api.materials import router as materials_router
from app.api.decor_presets import router as decor_presets_router

# ===== APP =====
app = FastAPI(
    title="Graffi Tech Mat API",
    version="1.0.0",
)

# ===== CORS =====
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5174",
        "http://127.0.0.1:5174",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ===== STARTUP =====
@app.on_event("startup")
def startup():
    validate_settings()
    Base.metadata.create_all(bind=engine)

# ===== ROUTERS (ORDER MATTERS) =====

app.include_router(auth_router)
app.include_router(users_router)
app.include_router(projects_router)
app.include_router(workspace_router)

app.include_router(public_router)

app.include_router(jobs_router)
app.include_router(models_router)
app.include_router(assets_router)

app.include_router(phase_i_mutations_router)

app.include_router(decor_exterior_router)
app.include_router(tuning_router)
app.include_router(body_router)

app.include_router(scenes_router)

app.include_router(upload_router)
app.include_router(presign_router)
app.include_router(admin_router)
app.include_router(audit_router)

# ✅ Snapshot mutation layers (ALL preserved)
app.include_router(snapshot_mutations_router)
app.include_router(snapshot_mutations_legacy_router)
app.include_router(snapshots_legacy_router)

app.include_router(snapshots_transform_router)
app.include_router(resolve_target_router)
app.include_router(snapshots_validate_transform_router)

# 📦 Phase M / N
app.include_router(exports_router)
app.include_router(distributions_router)

app.include_router(organizations_router)
app.include_router(signed_url_router)

# Snapshots (Phase 3 → 4.5)
app.include_router(snapshots_router)
app.include_router(snapshots_undo_redo_router)

@app.get("/health")
def health():
    return {"status": "ok"}

# 🧭 Studio kernel exposure (Phase E)
app.include_router(studio_state_router)          # E.1
app.include_router(studio_tools_router)          # E.2
app.include_router(studio_flow_router)           # E.2
app.include_router(studio_snapshot_state_router) # E.3
app.include_router(studio_audit_router)          # E.3

app.include_router(warehouse_router)
app.include_router(exports_images_router)
app.include_router(dashboard_router)
app.include_router(materials_router)
app.include_router(decor_presets_router)


