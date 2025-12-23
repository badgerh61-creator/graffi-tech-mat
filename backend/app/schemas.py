# backend/app/schemas.py

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
    processed: bool
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
    created_at: datetime
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


class TokenPair(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class RefreshTokenRequest(BaseModel):
    refresh_token: str

