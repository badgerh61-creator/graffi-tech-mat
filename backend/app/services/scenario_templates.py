from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional


@dataclass(frozen=True)
class ScenarioTemplate:
    key: str
    name: str
    version: str  # e.g. "v1"
    extends: Optional[str]
    defaults: Dict[str, Any]


# Built-in templates (deterministic, small JSON)
TEMPLATES: Dict[str, ScenarioTemplate] = {
    "accel_0_60_v1": ScenarioTemplate(
        key="accel_0_60_v1",
        name="0–60 Acceleration (Baseline)",
        version="v1",
        extends=None,
        defaults={
            "duration_s": 10.0,
            "timestep_s": 0.1,
            "throttle": 0.85,
            "gear_ratio": 10.0,
            "mass_kg": 1200.0,
        },
    ),
    "hill_climb_v1": ScenarioTemplate(
        key="hill_climb_v1",
        name="Hill Climb (Load + Drag)",
        version="v1",
        extends="accel_0_60_v1",
        defaults={
            # extends accel defaults, overrides a couple
            "throttle": 0.75,
            "mass_kg": 1400.0,
        },
    ),
    "thermal_load_v1": ScenarioTemplate(
        key="thermal_load_v1",
        name="Thermal Load (Sustained Throttle)",
        version="v1",
        extends=None,
        defaults={
            "duration_s": 120.0,
            "timestep_s": 0.5,
            "throttle": 0.70,
            "gear_ratio": 9.0,
            "mass_kg": 1200.0,
        },
    ),
    "endurance_v1": ScenarioTemplate(
        key="endurance_v1",
        name="Endurance (Long Run)",
        version="v1",
        extends="thermal_load_v1",
        defaults={
            "duration_s": 600.0,
            "timestep_s": 1.0,
            "throttle": 0.60,
        },
    ),
}


def list_templates() -> List[Dict[str, Any]]:
    # deterministic ordering by key
    out = []
    for k in sorted(TEMPLATES.keys()):
        t = TEMPLATES[k]
        out.append(
            {
                "key": t.key,
                "name": t.name,
                "version": t.version,
                "extends": t.extends,
                "defaults": t.defaults,
            }
        )
    return out


def _resolve_template_chain(template_key: str) -> List[ScenarioTemplate]:
    """
    Returns inheritance chain base->...->leaf deterministically.
    """
    if template_key not in TEMPLATES:
        raise KeyError(f"Unknown template_key '{template_key}'")

    chain: List[ScenarioTemplate] = []
    seen = set()
    cur = TEMPLATES[template_key]

    while cur is not None:
        if cur.key in seen:
            raise ValueError("Template inheritance cycle detected")
        seen.add(cur.key)
        chain.append(cur)
        cur = TEMPLATES.get(cur.extends) if cur.extends else None

    chain.reverse()
    return chain


def materialize_template(*, template_key: str, overrides: Dict[str, Any] | None) -> Dict[str, Any]:
    """
    Deterministic merge:
      base.defaults -> ... -> leaf.defaults -> overrides
    """
    chain = _resolve_template_chain(template_key)
    out: Dict[str, Any] = {}
    for t in chain:
        out.update(t.defaults or {})
    if overrides:
        out.update(overrides)
    return out


def get_template_meta(template_key: str) -> ScenarioTemplate:
    if template_key not in TEMPLATES:
        raise KeyError(f"Unknown template_key '{template_key}'")
    return TEMPLATES[template_key]
