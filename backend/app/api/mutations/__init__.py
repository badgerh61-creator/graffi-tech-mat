# app/api/mutations/__init__.py
from app.api.mutations.mutations import router
from app.api.mutations.public_router import public_router
from app.api.mutations.body.router import router as body_router

__all__ = [
    "router",
    "public_router",
    "body_router",
]

