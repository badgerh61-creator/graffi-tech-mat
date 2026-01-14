# app/schemas/snapshots.py
from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class SnapshotCreate(BaseModel):
    scene_state_hash: str
    render_profile: str


class SnapshotRead(BaseModel):
    id: int
    project_id: int
    scene_state_hash: str
    render_profile: str
    image_url: Optional[str]
    engine_version: str
    status: str
    error_message: Optional[str]
    created_at: datetime

    class Config:
        orm_mode = True

