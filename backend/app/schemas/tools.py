from __future__ import annotations

from pydantic import BaseModel, Field
from typing import Any, Dict


class ToolExecutePayload(BaseModel):
    target_id: str = Field(..., min_length=1)
    params: Dict[str, Any] = Field(default_factory=dict)


class ToolExecuteRequest(BaseModel):
    snapshot_id: int
    station: str = Field(..., min_length=1)
    tool: str  # ← allow ALL tools
    payload: Dict[str, Any]


class ToolExecuteResponse(BaseModel):
    new_snapshot_id: int
