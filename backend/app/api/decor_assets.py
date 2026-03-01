from __future__ import annotations
from fastapi import APIRouter
from app.services.decals.asset_registry import list_decal_assets

router = APIRouter(prefix="/decor", tags=["decor-assets"])

@router.get("/decal-assets")
def decal_assets():
    return {"assets": list_decal_assets()}
