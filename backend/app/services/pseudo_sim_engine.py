from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List
import math

@dataclass(frozen=True)
class PseudoSimScenario:
    duration_s: float
    timestep_s: float
    throttle: float
    gear_ratio: float
    mass_kg: float

def run_pseudo_sim(*, scenario: PseudoSimScenario) -> Dict[str, List[float]]:
    dt = scenario.timestep_s
    n = int(math.floor(scenario.duration_s / dt)) + 1

    time_s: List[float] = []
    speed: List[float] = []
    rpm: List[float] = []
    temp: List[float] = []
    grip: List[float] = []

    v = 0.0
    tC = 80.0

    base_accel = 6.0
    drag = 0.08
    heat_gain = 2.5
    heat_cool = 0.15

    for i in range(n):
        ts = i * dt
        time_s.append(round(ts, 6))

        a = (base_accel * scenario.throttle) - (drag * v)
        v = max(0.0, v + a * dt)

        r = max(800.0, v * scenario.gear_ratio * 120.0)
        tC = tC + (heat_gain * scenario.throttle + 0.00005 * r - heat_cool) * dt

        g = max(0.4, min(1.0, 1.0 - 0.01 * v))

        speed.append(round(v, 6))
        rpm.append(round(r, 3))
        temp.append(round(tC, 3))
        grip.append(round(g, 6))

    return {
        "time_s": time_s,
        "speed_mps": speed,
        "rpm": rpm,
        "engine_temp_c": temp,
        "grip": grip,
    }
