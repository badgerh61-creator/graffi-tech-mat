import pytest

def test_undo_blocked_at_root_snapshot(
    client,
    root_snapshot,
    editor_user,
):
    res = client.post(
        f"/projects/{root_snapshot.project_id}/snapshots/{root_snapshot.id}/undo",
        headers=auth(editor_user),
    )

    assert res.status_code == 409

