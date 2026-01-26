import pytest
from fastapi import HTTPException

def test_ai_viewer_cannot_propose(
    assistant_service,
    viewer_user,
    snapshot,
):
    with pytest.raises(HTTPException):
        assistant_service.handle_request(
            user=viewer_user,
            snapshot=snapshot,
            mode="proposal",
            prompt="Change panel rake",
        )
