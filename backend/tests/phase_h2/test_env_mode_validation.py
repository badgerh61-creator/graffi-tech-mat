import pytest
from app.core.env_modes import validate_env_mode

def test_env_mode_validation_rejects_invalid(monkeypatch):
    monkeypatch.setenv("ENV", "invalid-env")
    with pytest.raises(RuntimeError):
        validate_env_mode()

