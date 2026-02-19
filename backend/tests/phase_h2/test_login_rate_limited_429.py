def test_login_rate_limited_429(client, monkeypatch):
    monkeypatch.setenv("LOGIN_RATE_LIMIT_MAX", "2")
    monkeypatch.setenv("LOGIN_RATE_LIMIT_WINDOW_SECONDS", "60")

    # your login returns 401 on bad creds; that’s fine — limiter should still trip to 429
    client.post("/login", data={"username": "x", "password": "y"})
    client.post("/login", data={"username": "x", "password": "y"})
    r3 = client.post("/login", data={"username": "x", "password": "y"})

    assert r3.status_code == 429

