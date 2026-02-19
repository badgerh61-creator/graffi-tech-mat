from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.api.health import router as health_router
from app.db.session import get_db


class BrokenDB:
    def execute(self, *_args, **_kwargs):
        raise Exception("db down")


def test_ready_endpoint_db_down_returns_503():
    app = FastAPI()
    app.include_router(health_router)

    def override_get_db():
        yield BrokenDB()

    app.dependency_overrides[get_db] = override_get_db

    client = TestClient(app)
    r = client.get("/ready")
    assert r.status_code == 503
    assert r.json()["detail"] == "DB not ready"

