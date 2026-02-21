def test_ready_returns_true_when_db_ok(client):
    r = client.get("/ready")
    assert r.status_code == 200
    data = r.json()
    assert data["ready"] is True
    assert "db" in data["checks"]
    assert data["checks"]["db"]["ok"] is True
