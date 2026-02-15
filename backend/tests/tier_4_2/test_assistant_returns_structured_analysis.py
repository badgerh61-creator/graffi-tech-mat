def test_assistant_returns_structured_analysis(
    client,
    draft_snapshot,
    editor_user,
):
    response = client.post(
        f"/snapshots/{draft_snapshot.id}/assistant/tuning",
        headers=auth(editor_user),
        json={"mode": "inquiry"},
    )

    assert response.status_code == 200
    data = response.json()

    assert "analysis" in data
    assert "recommendations" in data
    assert "confidence" in data

