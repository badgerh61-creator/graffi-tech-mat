# backend/app/main.py

from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings, validate_settings
from app.db.base import Base
from app.db.session import engine

# ===== API ROUTERS =====
from app.api import (
    auth,
    users,
    models,
    assets,
    upload,
    presign,
    admin,
    audit,
    exports,
    organizations,   # 🆕 F2.3
    jobs,             # 🆕 Phase H3
)

app = FastAPI(
    title="Graffi Tech Mat API",
    version="1.0.0",
)

# ===== CORS (FIXED — CREDENTIAL SAFE) =====
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
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(models.router)
app.include_router(assets.router)
app.include_router(upload.router)
app.include_router(presign.router)

# 🧩 PHASE H3 — ASYNC JOB SURFACE (READ-ONLY)
app.include_router(jobs.router)

# 🔐 ADMIN / OPS
app.include_router(admin.router)
app.include_router(audit.router)
app.include_router(exports.router)

# 🏢 ORGANIZATIONS (F2.3)
app.include_router(organizations.router)

# ===== HEALTH =====
@app.get("/health")
def health():
    return {"status": "ok"}

