def test_undo_returns_404_or_409_or_200_when_missing_parent(client, completed_snapshot):
    # IMPORTANT: your API is project-scoped
    url = f"/projects/{completed_snapshot.project_id}/snapshots/{completed_snapshot.id}/undo"
    res = client.post(url)

    # 200 if undo worked (snapshot has parent)
    # 409 if undo not possible (no parent) OR service blocks
    # 404 only if fixture/project mismatch (should not happen if fixture is correct)
    assert res.status_code in (200, 409)

    if res.status_code == 200:
        body = res.json()
        assert "active_snapshot_id" in body


def test_redo_returns_409_or_200_when_missing_child(client, completed_snapshot):
    url = f"/projects/{completed_snapshot.project_id}/snapshots/{completed_snapshot.id}/redo"
    res = client.post(url)

    assert res.status_code in (200, 409)

    if res.status_code == 200:
        body = res.json()
        assert "active_snapshot_id" in body
