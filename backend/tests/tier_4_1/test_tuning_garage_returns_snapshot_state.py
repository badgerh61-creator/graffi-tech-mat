def test_tuning_garage_returns_snapshot_state(
    client,
    draft_snapshot,
    editor_user,
):
    response = client.get(
        f"/snapshots/{draft_snapshot.id}/tuning",
        headers=auth(editor_user),
    )

    assert response.status_code == 200
    data = response.json()

    assert "engine" in data
    assert "suspension" in data
    assert "wheels" in data

