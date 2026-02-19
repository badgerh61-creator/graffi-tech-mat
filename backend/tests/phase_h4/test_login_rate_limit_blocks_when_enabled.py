from fastapi.testclient import TestClient

def test_login_rate_limit_blocks_when_enabled(monkeypatch):
    monkeypatch.setenv("GTM_ENABLE_LOGIN_RATE_LIMIT", "true")
    monkeypatch.setenv("GTM_LOGIN_RL_WINDOW_SECONDS", "60")
    monkeypatch.setenv("GTM_LOGIN_RL_MAX_REQUESTS", "2")

    from app.main import create_app
    client = TestClient(create_app())

    body = {"username": "admin_phase_i@test.com", "password": "admin123"}

    r1 = client.post("/login", data=body)
    r2 = client.post("/login", data=body)
    r3 = client.post("/login", data=body)

    assert r1.status_code in (200, 401)
    assert r2.status_code in (200, 401)
    assert r3.status_code == 429
    assert r3.json()["detail"] == "Rate limit exceeded"

