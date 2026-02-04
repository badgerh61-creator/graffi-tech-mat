# backend/app/services/tool.py

from dataclasses import dataclass
from typing import Set
from app.studio.stations import StudioStation
from app.studio.modes import StudioMode


@dataclass(frozen=True)
class ToolDefinition:
    name: str
    operation: str
    required_station: StudioStation
    allowed_snapshot_statuses: Set[str]
    required_capability: str

    # 🔒 Phase E compatibility adapter
    def allowed_in_mode(self, mode: str) -> bool:
        """
        Phase E read-only compatibility.
        Phase T authority is stricter; this is a projection.
        """

        # read-only mode → no mutating tools
        if mode == StudioMode.read_only.value:
            return False

        # review mode → only finalize allowed
        if mode == StudioMode.review.value:
            return self.operation == "snapshot.finalize"

        # editing mode → allow draft tools
        return True

