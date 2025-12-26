from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings, validate_settings
from app.db.session import Base, engine

# ===== API ROUTERS =====
from app.api import (
    auth,
    users,
    models,
    assets,
    upload,
    presign,
    admin,
    audit,     # 🔵 Phase 8 — Audit Logs
    activity,  # 🟢 Phase F1 — Activity Feed
)

app = FastAPI(
    title="Graffi Tech Mat API",
    version="1.0.0",
)

# ===== CORS =====
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
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

# 🔐 ADMIN
app.include_router(admin.router)

# 🔵 Phase 8 — Admin Audit Log UI
app.include_router(audit.router)

# 🟢 Phase F1 — User Activity Feed
app.include_router(activity.router)

# ===== HEALTH =====
@app.get("/health")
def health():
    return {"status": "ok"}

