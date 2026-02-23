import pytest
from fastapi import HTTPException
from app.services.transform_with_snapping import normalize_transform_payload_with_snapping

def test_snapping_rejects_unknown_frame():
    with pytest.raises(HTTPException) as exc:
        normalize_transform_payload_with_snapping(
            payload={"snap": True, "frame_id": "not_real", "snap_step": 0.1, "x": 1.23}
        )
    assert exc.value.status_code == 422
