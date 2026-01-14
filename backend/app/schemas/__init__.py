# =========================================
# SAFE RE-EXPORTS — Phase S1.x
# Legacy first, domain overrides last
# =========================================

# ---- Legacy schemas (fallback only) ----
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

# ---- New modular schemas (AUTHORITATIVE) ----

# Users / Auth
from app.schemas.users import UserCreate, UserRead
from app.schemas.auth import Token, TokenPair, RefreshTokenRequest

# Assets
from app.schemas.assets import AssetCreate, AssetRead

# Models
from app.schemas.models import ModelBase, ModelCreate, ModelRead

# Projects 
from app.schemas.projects import ProjectCreate, ProjectRead

# Snapshots
from app.schemas.snapshots import SnapshotCreate, SnapshotRead

# Workspace
from app.schemas.workspace import WorkspaceCapabilities, WorkspaceRead

# Organizations
from app.schemas.organizations import (
    OrganizationCreate,
    OrganizationRead,
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

