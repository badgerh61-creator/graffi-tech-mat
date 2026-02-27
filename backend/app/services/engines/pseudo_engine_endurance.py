from __future__ import annotations

from typing import Any, Dict, List
import math


class PseudoEnduranceEngine:
    engine_version = "pseudo-endurance-v1"

    def run(self, *, snapshot_id: int, scenario: Dict[str, Any]) -> Dict[str, Any]:
        # read scenario with safe defaults
        duration_s = float(scenario.get("duration_s", 600.0))
        timestep_s = float(scenario.get("timestep_s", 1.0))
        throttle = float(scenario.get("throttle", 0.65))
        gear_ratio = float(scenario.get("gear_ratio", 9.0))
        mass_kg = float(scenario.get("mass_kg", 1200.0))

        thermal_ceiling = float(scenario.get("thermal_ceiling_c", 130.0))
        degradation_rate = float(scenario.get("degradation_rate", 0.0008))  # per second

        if duration_s <= 0 or timestep_s <= 0:
            raise ValueError("duration_s and timestep_s must be > 0")

        dt = timestep_s
        n = int(math.floor(duration_s / dt)) + 1

        time_s: List[float] = []
        speed: List[float] = []
        rpm: List[float] = []
        temp: List[float] = []
        grip: List[float] = []

        # baseline state
        v = 0.0
        tC = 85.0
        g = 1.0

        # deterministic constants
        base_accel = 5.5
        drag = 0.09

        # thermal approach rate to ceiling (exponential)
        heat_rate = 0.035   # higher -> faster saturation
        cool_bias = 0.08    # baseline cooling

        for i in range(n):
            ts = i * dt
            time_s.append(round(ts, 6))

            # degradation: grip decays slowly with time + throttle
            g = max(0.2, min(1.0, g - degradation_rate * dt * (0.4 + 0.6 * throttle)))

            # thermal saturation toward ceiling
            # dt*(rate*(ceiling - temp)) plus throttle heating minus cool bias
            tC = tC + (heat_rate * (thermal_ceiling - tC) + 1.8 * throttle - cool_bias) * dt
            tC = max(0.0, min(2000.0, tC))

            # power fade with temperature + grip (simple deterministic)
            temp_penalty = max(0.6, 1.0 - (max(0.0, tC - 110.0) * 0.002))
            power = throttle * temp_penalty * (0.7 + 0.3 * g)

            a = (base_accel * power) - (drag * v) - (0.0005 * mass_kg / 1000.0)
            v = max(0.0, v + a * dt)

            r = max(800.0, v * gear_ratio * 120.0)

            speed.append(round(v, 6))
            rpm.append(round(r, 3))
            temp.append(round(tC, 3))
            grip.append(round(g, 6))

        return {
            "timestep_s": timestep_s,
            "duration_s": duration_s,
            "curves": {
                "time_s": time_s,
                "speed_mps": speed,
                "rpm": rpm,
                "engine_temp_c": temp,
                "grip": grip,
            },
            "meta": {
                "mode": "endurance",
                "model_version": "pseudo-endurance-v1",
                "notes": "thermal saturation + grip degradation + power fade",
            },
        }
