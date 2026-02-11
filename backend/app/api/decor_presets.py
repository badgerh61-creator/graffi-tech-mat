from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.services.decor_library import list_decor_presets

router = APIRouter(prefix="/decor-presets", tags=["decor-presets"])

@router.get("/")
def get_decor_presets(
    culture_pack: str | None = None,
    page: int = 1,
    pageSize: int = 50,
    db: Session = Depends(get_db),
):
    return list_decor_presets(
        db=db,
        culture_pack=culture_pack,
        page=page,
        page_size=pageSize,
    )

