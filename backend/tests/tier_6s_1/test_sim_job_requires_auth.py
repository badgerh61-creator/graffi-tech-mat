from fastapi import HTTPException
from app.api.deps import get_current_user
from app.main import app


def test_sim_job_requires_auth(client, draft_snapshot):
    # Force unauth for this test, even if conftest auto-auths the client.
    app.dependency_overrides[get_current_user] = lambda: (_ for _ in ()).throw(
        HTTPException(status_code=401, detail="Not authenticated")
    )

    try:
        r = client.post("/simulation/jobs", json={"snapshot_id": draft_snapshot.id})
        assert r.status_code in (401, 403)
    finally:
        app.dependency_overrides.pop(get_current_user, None)
