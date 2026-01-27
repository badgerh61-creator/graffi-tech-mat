import pytest
from fastapi import HTTPException
from app.services.mode_guard import require_mode_allows_tool

def test_read_only_blocks_execution():
    with pytest.raises(HTTPException):
        require_mode_allows_tool(
            mode="read_only",
            tool="validate",
        )

