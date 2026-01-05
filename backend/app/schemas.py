# backend/app/schemas.py
# =========================================
# Graffi-Tech-Mat — Pydantic Schemas
# Phase 4.6 — SAFE RESTORE + ROLE SUPPORT
# =========================================

from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

# ======================
# ASSETS
# ======================

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
    processed: bool = False   # SAFE DEFAULT
    created_at: datetime

    class Config:
        orm_mode = True


# ======================
# MODELS
# ======================

class ModelBase(BaseModel):
    name: str
    description: Optional[str] = None


class ModelCreate(ModelBase):
    pass


class ModelRead(ModelBase):
    id: int
    owner_id: int
    created_at: datetime
    role: str                      # ✅ Phase 2A
    assets: List[AssetRead] = []

    class Config:
        orm_mode = True


# ======================
# PRESIGNED URL
# ======================

class PresignResponse(BaseModel):
    url: str
    fields: Optional[dict] = None
    expire_seconds: Optional[int] = None


# ======================
# USERS
# ======================

class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserRead(BaseModel):
    id: int
    email: EmailStr
    is_admin: bool
    created_at: datetime

    class Config:
        orm_mode = True


# ======================
# AUTH / TOKENS
# ======================

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenPair(BaseModel):         # 🔥 RESTORED — REQUIRED BY /login
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class RefreshTokenRequest(BaseModel):
    refresh_token: str


# ======================
# ORGANIZATIONS
# ======================

class OrganizationCreate(BaseModel):
    name: str


class OrganizationRead(BaseModel):
    id: int
    name: str
    created_at: datetime

    class Config:
        orm_mode = True


# ======================
# RENDERED SNAPSHOTS
# ======================

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


# ======================
# PROJECTS
# ======================

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


# ======================
# WORKSPACE (READ-ONLY)
# ======================

class WorkspaceRead(BaseModel):
    project: ProjectRead
    snapshots: List[SnapshotRead]
    assets: List[AssetRead]

    class Config:
        orm_mode = True

