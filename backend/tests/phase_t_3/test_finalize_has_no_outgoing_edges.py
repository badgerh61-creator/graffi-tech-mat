import pytest
from fastapi import HTTPException
from app.services.flow_guard import require_flow_allowed

def test_finalize_has_no_outgoing_edges():
    with pytest.raises(HTTPException):
        require_flow_allowed(
            current_state="finalize",
            next_tool="transform",
        )

