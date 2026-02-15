import pytest

def test_assistant_invalid_mode_rejected(
    client,
    draft_snapshot,
    editor_user,
):
    response = client.post(
        f"/snapshots/{draft_snapshot.id}/assistant/tuning",
        headers=auth(editor_user),
        json={"mode": "auto_apply"},
    )

    assert response.status_code == 422

