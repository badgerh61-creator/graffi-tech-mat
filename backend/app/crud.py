# =========================================
# SAFE RE-EXPORTS — Phase S2 (CRUD)
# Legacy compatibility layer
# DO NOT place logic here
# =========================================

# ---- Users ----
from app.crud.users import (
    get_user_by_email,
    get_user_by_id,
)

# ---- Assets ----
from app.crud.assets import (
    create_asset,
)

# ---- Models ----
from app.crud.models import (
    create_model,
    get_model_by_id,
    require_owner,
    require_model_role,
    resolve_user_role_for_model,
    get_models_accessible_to_user,
    get_model_if_accessible,
)

# ---- Projects ----
from app.crud.projects import (
    require_project_role,
)

# ---- Invites ----
from app.crud.invites import (
    get_invite_by_token,
    create_model_invite,
    accept_model_invite,
)

# ---- Jobs ----
from app.crud.jobs import (
    create_job,
)

