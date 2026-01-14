# =========================================
# SAFE RE-EXPORTS — Phase S1.2
# DO NOT REMOVE legacy names yet
# =========================================

# ---- New modular schemas (authoritative) ----
from app.schemas.users import UserCreate, UserRead
from app.schemas.auth import Token, TokenPair, RefreshTokenRequest

# ---- Legacy schemas (still defined here for now) ----
from app.schemas.legacy import (
    AssetBase,
    AssetCreate,
    AssetRead,
    ModelBase,
    ModelCreate,
    ModelRead,
    PresignResponse,
    OrganizationCreate,
    OrganizationRead,
    SnapshotCreate,
    SnapshotRead,
    ProjectCreate,
    ProjectRead,
    WorkspaceCapabilities,
    WorkspaceRead,
)

__all__ = [
    # Users / Auth
    "UserCreate",
    "UserRead",
    "Token",
    "TokenPair",
    "RefreshTokenRequest",

    # Assets
    "AssetBase",
    "AssetCreate",
    "AssetRead",

    # Models
    "ModelBase",
    "ModelCreate",
    "ModelRead",

    # Misc
    "PresignResponse",
    "OrganizationCreate",
    "OrganizationRead",
    "SnapshotCreate",
    "SnapshotRead",
    "ProjectCreate",
    "ProjectRead",
    "WorkspaceCapabilities",
    "WorkspaceRead",
]

