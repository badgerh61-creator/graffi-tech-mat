from dataclasses import dataclass
from typing import Set
from app.studio.stations import StudioStation

@dataclass(frozen=True)
class ToolDefinition:
    name: str
    operation: str
    required_station: StudioStation
    allowed_snapshot_statuses: Set[str]
    required_capability: str

