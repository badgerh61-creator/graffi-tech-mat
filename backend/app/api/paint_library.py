from __future__ import annotations
from fastapi import APIRouter
from app.services.materials.paint_library import list_paint_library

router = APIRouter(prefix="/materials", tags=["paint-library"])

@router.get("/paint-library")
def get_paint_library():
    return {"presets": list_paint_library()}
