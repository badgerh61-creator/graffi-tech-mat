from app.services import ops_checks

def test_ready_returns_not_ready_when_db_fails(client, monkeypatch):
    def _fail(_db):
        return ops_checks.ReadinessResult(
            ready=False,
            checks={"db": {"ok": False, "detail": "db_error:OperationalError"}},
        )

    monkeypatch.setattr(ops_checks, "compute_readiness", lambda db: _fail(db))

    r = client.get("/ready")
    assert r.status_code == 200
    data = r.json()
    assert data["ready"] is False
    assert data["checks"]["db"]["ok"] is False
