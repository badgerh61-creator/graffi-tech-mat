from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.db.session import get_db
from app.models.asset import Asset
from pydantic import BaseModel

class AssetOut(BaseModel):
    id: str
    name: str
    type: str
    url: str
    thumbnail_url: str | None
    size: int
    meta: dict | None

    class Config:
        orm_mode = True

router = APIRouter(prefix="/assets", tags=["assets"])

@router.get("/", response_model=List[AssetOut])
def list_assets(db: Session = Depends(get_db)):
    return db.query(Asset).order_by(Asset.created_at.desc()).all()
