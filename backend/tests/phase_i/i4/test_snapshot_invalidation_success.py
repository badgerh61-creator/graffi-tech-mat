def test_invalidate_completed_snapshot(
    client,
    db,
    completed_snapshot,
):
    response = client.post(
        f"/snapshots/{completed_snapshot.id}/mutations/invalidate"
    )

    assert response.status_code == 200

    db.refresh(completed_snapshot)
    assert completed_snapshot.status == "obsolete"

