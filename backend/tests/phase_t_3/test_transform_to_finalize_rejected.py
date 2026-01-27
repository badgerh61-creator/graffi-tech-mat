import pytest
from fastapi import HTTPException
from app.services.flow_guard import require_flow_allowed

def test_transform_to_finalize_rejected():
    with pytest.raises(HTTPException) as exc:
        require_flow_allowed(
            current_state="transform",
            next_tool="finalize",
        )

    assert exc.value.status_code == 409

