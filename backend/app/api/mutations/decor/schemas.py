from pydantic import BaseModel
from typing import Dict, Any


class ApplyExteriorDecalPayload(BaseModel):
    project_id: int
    snapshot_base_id: int
    decal_id: str
    target: Dict[str, Any]

