from __future__ import annotations

from typing import Any, Dict

from app.services.pseudo_sim_engine import PseudoSimScenario, run_pseudo_sim


class PseudoEngine:
    engine_version = "pseudo-v1"

    def run(self, *, snapshot_id: int, scenario: Dict[str, Any]) -> Dict[str, Any]:
        sc = PseudoSimScenario(
            duration_s=float(scenario.get("duration_s", 10.0)),
            timestep_s=float(scenario.get("timestep_s", 0.1)),
            throttle=float(scenario.get("throttle", 0.6)),
            gear_ratio=float(scenario.get("gear_ratio", 10.0)),
            mass_kg=float(scenario.get("mass_kg", 1200.0)),
        )

        curves = run_pseudo_sim(scenario=sc)

        return {
            "timestep_s": float(sc.timestep_s),
            "duration_s": float(sc.duration_s),
            "curves": curves,
        }
