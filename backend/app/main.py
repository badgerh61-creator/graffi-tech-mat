from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from .core.config import settings, validate_settings
from .db.session import Base, engine

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Admin panel – OPTIONAL during Docker development
# app.mount('/admin', StaticFiles(directory='frontend/admin/dist', html=True), name='admin')

@app.on_event("startup")
def startup():
    validate_settings()
    Base.metadata.create_all(bind=engine)


# Health check
@app.get("/health")
def health():
    return {"status": "ok"}

