import pytest
from app.models.curve import Curve

@pytest.fixture
def curve(db, draft_snapshot):
    """
    Minimal parametric curve attached to a draft snapshot.
    Geometry is irrelevant in J.2 — intent only.
    """
    curve = Curve(
        snapshot_id=draft_snapshot.id,
        curve_type="polyline",              # ✅ MATCHES MODEL
        reference_plane_id="vehicle_centerline",
        params={
            "points": [
                {"x": 0, "y": 0},
                {"x": 100, "y": 0},
            ]
       },
       constraints=[],
    )

    db.add(curve)
    db.commit()
    db.refresh(curve)
    return curve

