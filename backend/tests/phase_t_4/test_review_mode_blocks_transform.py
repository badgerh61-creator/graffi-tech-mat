import pytest
from fastapi import HTTPException
from app.services.mode_guard import require_mode_allows_tool

def test_review_mode_blocks_transform():
    with pytest.raises(HTTPException):
        require_mode_allows_tool(
            mode="review",
            tool="transform",
        )

