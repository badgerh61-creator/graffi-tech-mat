from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.db.session import Base, engine

# Auto-create DB tables on startup (safe for dev)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Graffi Backend - Standard Production")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
from app.api import upload, assets, models, presign, presets

app.include_router(upload.router)
app.include_router(assets.router)
app.include_router(models.router)
app.include_router(presign.router)
app.include_router(presets.router)

@app.get("/health")
def health():
    return {"status": "ok", "env": settings.ENV}
