from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.api.deps import get_current_user
from app.services.performance_metrics import compute_performance_metrics
from app.models.rendered_snapshot import RenderedSnapshot as Snapshot


router = APIRouter(prefix="/snapshots", tags=["metrics"])


@router.get("/{snapshot_id}/metrics/performance")
def get_performance_metrics(
    snapshot_id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    snapshot = db.get(Snapshot, snapshot_id)
    if not snapshot:
        raise HTTPException(404, "Snapshot not found")

    # Vehicle constants optional; keep it deterministic
    vehicle = {
        "mass_kg": getattr(snapshot, "vehicle_mass_kg", None),
    }

    metrics = compute_performance_metrics(
        tuning_state=snapshot.tuning_state or {},
        vehicle=vehicle,
    )

    # dataclass -> dict
    return {
        "power_hp": metrics.power_hp,
        "torque_nm": metrics.torque_nm,
        "power_to_weight_hp_per_ton": metrics.power_to_weight_hp_per_ton,
        "est_0_100_kph_seconds": metrics.est_0_100_kph_seconds,
        "est_top_speed_kph": metrics.est_top_speed_kph,
        "handling_index": metrics.handling_index,
        "braking_index": metrics.braking_index,
        "notes": metrics.notes,
        "confidence": metrics.confidence,
    }

