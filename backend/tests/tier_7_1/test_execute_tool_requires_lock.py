from fastapi import HTTPException


def test_execute_tool_requires_lock(
    client,
    draft_snapshot,
    editor_user,
    geometry_station,
    translate_request_payload,
    monkeypatch,
):
    # --- Allow Phase T evaluator ---
    class Allow:
        allowed = True
        reason = None

    monkeypatch.setattr(
        "app.services.studio_kernel_executor.evaluate_tool_invocation",
        lambda **kwargs: Allow(),
    )

    # --- Deny lock ---
    def deny_lock(**kwargs):
        raise HTTPException(403, "Draft ownership required")

    monkeypatch.setattr(
        "app.services.transform_tool_service._require_draft_lock_if_available",
        lambda **kwargs: deny_lock(**kwargs),
    )

    r = client.post(
        "/tools/execute",
        json={
            "snapshot_id": draft_snapshot.id,
            "station": geometry_station,
            "tool": "TRANSLATE",
            "payload": translate_request_payload,
        },
        headers=auth(editor_user),
    )

    assert r.status_code == 403
