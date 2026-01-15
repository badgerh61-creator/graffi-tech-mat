from app.api.deps import get_current_user

def test_body_capability_required(
    client,
    completed_snapshot,
    editor_user,
):
    client.app.dependency_overrides[get_current_user] = lambda: editor_user

    payload = {
        "project_id": completed_snapshot.project_id,
        "base_snapshot_id": completed_snapshot.id,
        "preset_id": "widebody_v1",
        "parameters": {},
    }

    res = client.post("/mutations/body/apply-morph", json=payload)
    assert res.status_code == 403

    client.app.dependency_overrides.clear()

