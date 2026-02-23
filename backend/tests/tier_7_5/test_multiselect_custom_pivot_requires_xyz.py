import pytest
from fastapi import HTTPException
from app.services.selection_payload import normalize_multiselect_payload

def test_multiselect_custom_pivot_requires_xyz():
    with pytest.raises(HTTPException) as exc:
        normalize_multiselect_payload(
            payload={
                "selected_target_ids": ["panel-1", "panel-2"],
                "pivot_mode": "custom",
                "pivot": {"x": 1, "y": 2},  # z missing
            }
        )
    assert exc.value.status_code == 422
