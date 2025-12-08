from fastapi import APIRouter, HTTPException, Depends
from typing import List
from pydantic import BaseModel
from app.db.session import get_db
from sqlalchemy.orm import Session
from app.db import models
import uuid

class PresetIn(BaseModel):
    name: str
    category: str = "custom"
    data: dict
    thumbnail: str | None = None

class PresetOut(BaseModel):
    id: str
    name: str
    category: str
    data: dict
    thumbnail: str | None = None

router = APIRouter(prefix="/presets", tags=["presets"])

@router.post("/save", response_model=dict)
def save_preset(req: PresetIn, db: Session = Depends(get_db)):
    pid = str(uuid.uuid4())
    from app.db.models import Asset as AssetModel
    asset = AssetModel(id=pid, name=req.name, type="preset", url="", thumbnail_url=req.thumbnail, meta={"data": req.data, "category": req.category})
    db.add(asset)
    db.commit()
    db.refresh(asset)
    return {"ok": True, "preset_id": asset.id}

@router.get("/", response_model=List[dict])
def list_presets(db: Session = Depends(get_db)):
    items = db.query(models.Asset).filter(models.Asset.type == "preset").order_by(models.Asset.created_at.desc()).all()
    return [{"id": i.id, "name": i.name, "category": i.meta.get("category"), "data": i.meta.get("data"), "thumbnail": i.thumbnail_url} for i in items]
