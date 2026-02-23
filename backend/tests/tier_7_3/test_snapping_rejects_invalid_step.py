import pytest
from fastapi import HTTPException
from app.services.snapping import apply_snapping_to_transform_payload

def test_snapping_rejects_invalid_step():
    with pytest.raises(HTTPException) as exc:
        apply_snapping_to_transform_payload(payload={"snap": True, "snap_step": 0})
    assert exc.value.status_code == 422
