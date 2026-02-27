from __future__ import annotations

from pydantic import BaseModel, Field
from typing import Any, Dict, List, Optional


class ScenarioCreateRequest(BaseModel):
    project_id: int
    name: str = Field(..., min_length=1, max_length=120)
    scenario: Dict[str, Any] = Field(default_factory=dict)


class ScenarioCreateResponse(BaseModel):
    scenario_id: int


class ScenarioListItem(BaseModel):
    id: int
    name: str
    scenario: Dict[str, Any]


class ScenarioListResponse(BaseModel):
    project_id: int
    scenarios: List[ScenarioListItem]


class RunCreateRequest(BaseModel):
    snapshot_id: int
    engine_version: str = "pseudo-v1"
    scenario_id: Optional[int] = None
    scenario: Optional[Dict[str, Any]] = None


class RunCreateResponse(BaseModel):
    run_id: int
    artifact_id: int


class RunListItem(BaseModel):
    run_id: int
    artifact_id: int
    snapshot_id: int
    scenario_id: Optional[int]
    engine_version: str


class RunListResponse(BaseModel):
    project_id: int
    runs: List[RunListItem]


class CompareMatrixRequest(BaseModel):
    artifact_ids: List[int] = Field(..., min_items=2)


class CompareMatrixResponse(BaseModel):
    artifact_ids: List[int]
    matrix: Dict[str, Dict[str, float]]
