# app/schemas/workspace.py
from pydantic import BaseModel
from typing import List

from app.schemas.projects import ProjectRead
from app.schemas.snapshots import SnapshotRead
from app.schemas.assets import AssetRead


class WorkspaceCapabilities(BaseModel):
    can_view_assets: bool
    can_view_snapshots: bool
    can_edit_project: bool


class WorkspaceRead(BaseModel):
    project: ProjectRead
    snapshots: List[SnapshotRead]
    assets: List[AssetRead]
    capabilities: WorkspaceCapabilities

    class Config:
        orm_mode = True

