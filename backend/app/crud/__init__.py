# Users
from app.crud.users import (
    get_user_by_email,
    get_user_by_id,
)

# Models (TEMP re-export until Phase S2.2 is complete)
from app.crud.models import (
    create_model,
    get_model_by_id,
    require_owner,
    require_model_role,
    resolve_user_role_for_model,
    get_models_accessible_to_user,
    get_model_if_accessible,
)

# Assets

from app.crud.assets import create_asset, transition_asset_status

# Projects
from app.crud.projects import require_project_role

# Jobs
from app.crud.jobs import create_job

# ---- Invites CRUD ----
from app.crud.invites import (
    get_invite_by_token,
    create_model_invite,
    accept_model_invite,
)

# Snapshots (Phase 4.x legacy support)
from app.crud.snapshots import get_snapshot_by_id

from app.crud.projects import get_projects_accessible_to_user

__all__ = [
    # Users
    "get_user_by_email",
    "get_user_by_id",

    # Models
    "create_model",
    "get_model_by_id",
    "require_owner",
    "require_model_role",
    "resolve_user_role_for_model",
    "get_models_accessible_to_user",
    "get_model_if_accessible",
    
        # Assets
    "create_asset",
    "transition_asset_status",

    # Snapshots
    "get_snapshot_by_id",
    
    "get_projects_accessible_to_user",
]

