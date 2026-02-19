def test_health_endpoint_alive(client):
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"

