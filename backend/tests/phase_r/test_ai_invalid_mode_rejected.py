import pytest
from fastapi import HTTPException

def test_ai_invalid_mode_rejected(
    assistant_service,
    editor_user,
    snapshot,
):
    with pytest.raises(HTTPException) as exc:
        assistant_service.handle_request(
            user=editor_user,
            snapshot=snapshot,
            mode="execute",
            prompt="Apply change",
        )

    assert exc.value.status_code == 422
