from pydantic import BaseModel
from typing import Dict, Any


class BodyMorphApplyPayload(BaseModel):
    project_id: int                # ✅ INT, NOT UUID
    base_snapshot_id: int           # ✅ INT, NOT UUID
    preset_id: str
    parameters: Dict[str, Any]

