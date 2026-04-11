from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.services.material_catalog import list_materials
from app.services.materials.presets import list_presets

router = APIRouter(prefix="/materials", tags=["materials"])


@router.get("/")
def get_materials(
    page: int = 1,
    pageSize: int = 50,
    db: Session = Depends(get_db),
):
    return list_materials(db, page=page, page_size=pageSize)


# Tier 7.42 — canonical preset source (NO DB)
@router.get("/presets")
def get_material_presets():
    return {
        "presets": list_presets()
    }
