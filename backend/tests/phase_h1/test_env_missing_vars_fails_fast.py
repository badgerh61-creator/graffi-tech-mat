import pytest
from app.core.env import validate_required_env

def test_env_missing_vars_fails_fast(monkeypatch):
    # delete a few hard requirements
    monkeypatch.delenv("DATABASE_URL", raising=False)
    monkeypatch.delenv("SECRET_KEY", raising=False)
    monkeypatch.delenv("MINIO_ENDPOINT", raising=False)

    with pytest.raises(RuntimeError) as exc:
        validate_required_env()

    msg = str(exc.value)
    assert "DATABASE_URL" in msg
    assert "SECRET_KEY" in msg
    assert "MINIO_ENDPOINT" in msg

