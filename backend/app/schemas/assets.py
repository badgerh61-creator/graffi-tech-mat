from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class AssetBase(BaseModel):
    filename: str
    content_type: Optional[str] = None
    size: Optional[int] = None

class AssetCreate(AssetBase):
    s3_key: str

class AssetRead(AssetBase):
    id: int
    s3_key: str
    thumbnail_key: Optional[str]
    processed: bool = False
    created_at: datetime

    class Config:
        orm_mode = True

