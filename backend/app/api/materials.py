from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.services.material_catalog import list_materials

router = APIRouter(prefix="/materials", tags=["materials"])

@router.get("/")
def get_materials(
    page: int = 1,
    pageSize: int = 50,
    db: Session = Depends(get_db),
):
    return list_materials(db, page=page, page_size=pageSize)

