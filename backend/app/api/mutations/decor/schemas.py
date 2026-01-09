from pydantic import BaseModel
from typing import Dict, Any


# -------------------------------------------------
# APPLY DECAL (Phase K.1)
# -------------------------------------------------

class ApplyExteriorDecalPayload(BaseModel):
    project_id: int
    snapshot_base_id: int
    decal_id: str
    target: Dict[str, Any]


# -------------------------------------------------
# REMOVE DECAL (Phase K.1)
# -------------------------------------------------

class RemoveExteriorDecalPayload(BaseModel):
    project_id: int
    snapshot_base_id: int
    decal_instance_id: str

