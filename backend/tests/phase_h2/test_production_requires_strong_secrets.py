import pytest
from app.core.env_modes import validate_production_requirements

def test_production_requires_strong_secrets(monkeypatch):
    monkeypatch.setenv("ENV", "production")
    monkeypatch.setenv("JWT_SECRET", "short")
    monkeypatch.setenv("JWT_REFRESH_SECRET", "short")
    monkeypatch.setenv("CORS_ALLOWLIST", "http://localhost:5174")

    with pytest.raises(RuntimeError):
        validate_production_requirements()

