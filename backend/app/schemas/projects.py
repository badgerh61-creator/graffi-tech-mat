from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class ProjectCreate(BaseModel):
    name: str = "Untitled Project"


class ProjectRead(BaseModel):
    id: int
    name: str
    owner_id: int
    active_snapshot_id: Optional[int]
    created_at: datetime

    class Config:
        orm_mode = True


