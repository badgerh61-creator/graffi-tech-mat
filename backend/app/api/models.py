from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional

from app.db.session import get_db
from app.models.model import Model
from pydantic import BaseModel

class ModelOut(BaseModel):
    id: str
    name: str
    asset_id: Optional[str]
    preview: Optional[str]
    meta: Optional[dict]
    created_at: Optional[str]

    class Config:
        orm_mode = True

router = APIRouter(prefix="/models", tags=["models"])

@router.get("/", response_model=List[ModelOut])
def list_models(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(Model).order_by(Model.created_at.desc()).offset(skip).limit(limit).all()

@router.get("/{model_id}", response_model=ModelOut)
def get_model(model_id: str, db: Session = Depends(get_db)):
    m = db.query(Model).filter(Model.id == model_id).first()
    if not m:
        raise HTTPException(status_code=404, detail="Model not found")
    return m
