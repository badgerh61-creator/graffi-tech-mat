from pydantic import BaseModel
from typing import Optional, Dict

# -----------------------------
# ASSET SCHEMAS
# -----------------------------
class AssetCreate(BaseModel):
    id: str
    name: str
    type: str
    url: str
    thumbnail_url: Optional[str] = None
    size: Optional[int] = 0
    meta: Optional[Dict] = {}

class AssetOut(BaseModel):
    id: str
    name: str
    type: str
    url: str
    thumbnail_url: Optional[str]
    size: int
    meta: Optional[Dict]
    created_at: Optional[str]

    class Config:
        orm_mode = True


# -----------------------------
# MODEL SCHEMAS
# -----------------------------
class ModelOut(BaseModel):
    id: str
    name: str
    asset_id: Optional[str]
    preview: Optional[str]
    meta: Optional[Dict]
    created_at: Optional[str]

    class Config:
        orm_mode = True
