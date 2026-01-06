# backend/app/main.py

from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import validate_settings
from app.db.base import Base
from app.db.session import engine

# ===== ROUTER IMPORTS (EXPLICIT & SAFE) =====
from app.api.auth import router as auth_router
from app.api.users import router as users_router
from app.api.projects import router as projects_router
from app.api.job import router as jobs_router
from app.api.models import router as models_router
from app.api.assets import router as assets_router
from app.api.upload import router as upload_router
from app.api.presign import router as presign_router
from app.api.mutations import router as mutations_router
from app.api.admin import router as admin_router
from app.api.audit import router as audit_router
from app.api.exports import router as exports_router
from app.api.organizations import router as organizations_router
from app.api.snapshots import (
    router as snapshots_router,
    mutation_router as snapshot_mutation_router,
)
from app.api.workspace import router as workspace_router

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

# ===== ROUTERS =====
app.include_router(auth_router)
app.include_router(users_router)
app.include_router(projects_router)
app.include_router(workspace_router)

app.include_router(jobs_router)
app.include_router(models_router)
app.include_router(assets_router)
app.include_router(mutations_router)

app.include_router(upload_router)
app.include_router(presign_router)

app.include_router(admin_router)
app.include_router(audit_router)
app.include_router(exports_router)
app.include_router(organizations_router)

# Phase J — project-scoped snapshot routes
app.include_router(snapshots_router)

# Phase I.4 — global snapshot mutation routes
app.include_router(snapshot_mutation_router)

# ===== HEALTH =====
@app.get("/health")
def health():
    return {"status": "ok"}

