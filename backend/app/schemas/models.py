from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

from app.schemas.assets import AssetRead


class ModelBase(BaseModel):
    name: str
    description: Optional[str] = None


class ModelCreate(ModelBase):
    pass


class ModelRead(ModelBase):
    id: int
    owner_id: int
    created_at: datetime
    role: str
    assets: List[AssetRead] = []

    class Config:
        orm_mode = True

