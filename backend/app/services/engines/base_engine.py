from __future__ import annotations

from typing import Any, Dict, Protocol


class SimulationEngine(Protocol):
    engine_version: str

    def run(self, *, snapshot_id: int, scenario: Dict[str, Any]) -> Dict[str, Any]:
        """
        Must return:
        {
          "timestep_s": float,
          "duration_s": float,
          "curves": dict
        }
        """
        ...
