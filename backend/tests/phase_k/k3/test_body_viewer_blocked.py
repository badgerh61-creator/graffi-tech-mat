from app.api.deps import get_current_user

def test_body_viewer_blocked(
    client,
    completed_snapshot,
    viewer_user,
):
    # 🔑 FORCE FastAPI to use viewer_user
    client.app.dependency_overrides[get_current_user] = lambda: viewer_user

    payload = {
        "project_id": completed_snapshot.project_id,
        "base_snapshot_id": completed_snapshot.id,
        "preset_id": "widebody_v1",
        "parameters": {},
    }

    res = client.post("/mutations/body/apply-morph", json=payload)
    assert res.status_code == 403

    # 🧹 Clean up
    client.app.dependency_overrides.clear()

