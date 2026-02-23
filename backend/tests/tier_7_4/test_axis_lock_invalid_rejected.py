import pytest
from fastapi import HTTPException
from app.services.axis_locks import apply_axis_lock_to_payload

def test_axis_lock_invalid_rejected():
    with pytest.raises(HTTPException) as exc:
        apply_axis_lock_to_payload(payload={"axis_lock": "nope", "x": 1})
    assert exc.value.status_code == 422
