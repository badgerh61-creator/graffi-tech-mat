import pytest
from fastapi import HTTPException
from app.services.selection_payload import normalize_multiselect_payload

def test_multiselect_requires_nonempty_list():
    with pytest.raises(HTTPException) as exc:
        normalize_multiselect_payload(payload={"selected_target_ids": []})
    assert exc.value.status_code == 422
