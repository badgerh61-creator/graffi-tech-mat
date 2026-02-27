from __future__ import annotations

from sqlalchemy.orm import Session
from app.models.simulation_run import SimulationRun

# Tier 6S.9 (safe import; only used if hashes provided)
try:
    from app.services.reproducibility import compute_run_fingerprint, is_verified_deterministic
except Exception:  # pragma: no cover
    compute_run_fingerprint = None
    is_verified_deterministic = None


def create_run_index(
    *,
    db: Session,
    project_id: int,
    snapshot_id: int,
    scenario_id: int | None,
    artifact_id: int,
    engine_version: str,
    user_id: int,

    # ---- Tier 6S.9 additive params (optional) ----
    snapshot_hash: str = "",
    scenario_hash: str = "",
) -> int:
    # Default-safe behavior: keep blank hashes if not provided.
    fp = ""
    verified = False

    if snapshot_hash and scenario_hash and compute_run_fingerprint and is_verified_deterministic:
        fp = compute_run_fingerprint(
            snapshot_hash=snapshot_hash,
            scenario_hash=scenario_hash,
            engine_version=engine_version,
            artifact_id=int(artifact_id),
        )
        verified = is_verified_deterministic(
            engine_version=engine_version,
            snapshot_hash=snapshot_hash,
            scenario_hash=scenario_hash,
        )

    row = SimulationRun(
        project_id=project_id,
        snapshot_id=snapshot_id,
        scenario_id=scenario_id,
        artifact_id=artifact_id,
        engine_version=engine_version,
        created_by=user_id,

        # Tier 6S.9 fields (safe defaults)
        snapshot_hash=snapshot_hash or "",
        scenario_hash=scenario_hash or "",
        run_fingerprint=fp or "",
        verified_deterministic=bool(verified),
    )
    db.add(row)
    db.commit()
    db.refresh(row)
    return int(row.id)


def list_runs(*, db: Session, project_id: int):
    rows = (
        db.query(SimulationRun)
        .filter(SimulationRun.project_id == project_id)
        .order_by(SimulationRun.id.asc())
        .all()
    )
    return [
        {
            "run_id": int(r.id),
            "artifact_id": int(r.artifact_id),
            "snapshot_id": int(r.snapshot_id),
            "scenario_id": int(r.scenario_id) if r.scenario_id is not None else None,
            "engine_version": r.engine_version,
            # (optional) expose repro fields later if you want—keeping old response stable for now
        }
        for r in rows
    ]
