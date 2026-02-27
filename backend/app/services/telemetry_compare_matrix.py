from __future__ import annotations

from typing import Dict, List
from fastapi import HTTPException

from app.services.telemetry_reports import compute_summary, compute_delta


def build_compare_matrix(*, artifacts: List[dict]) -> Dict[str, Dict[str, float]]:
    """
    artifacts: [{id, curves, timestep_s, duration_s}, ...]
    Deterministic ordering: id asc.
    matrix[field]["A-B"] = (B - A)
    """
    if len(artifacts) < 2:
        raise HTTPException(422, "artifact_ids must include at least 2")

    artifacts = sorted(artifacts, key=lambda a: int(a["id"]))
    summaries: Dict[int, Dict[str, float]] = {}

    for a in artifacts:
        aid = int(a["id"])
        summaries[aid] = compute_summary(
            curves=a["curves"],
            timestep_s=float(a["timestep_s"]),
            duration_s=float(a["duration_s"]),
        )

    ids = [int(a["id"]) for a in artifacts]
    fields = [
        "speed_max_mps", "speed_avg_mps",
        "rpm_max", "rpm_avg",
        "engine_temp_max_c", "engine_temp_avg_c",
        "grip_min", "grip_avg",
    ]

    out: Dict[str, Dict[str, float]] = {f: {} for f in fields}
    for i, a_id in enumerate(ids):
        for b_id in ids[i + 1 :]:
            delta = compute_delta(a_summary=summaries[a_id], b_summary=summaries[b_id])
            key = f"{a_id}-{b_id}"
            for f in fields:
                out[f][key] = float(delta[f])

    return out
