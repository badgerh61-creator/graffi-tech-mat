from app.models.journal_entry import JournalEntry

def test_export_request_is_journaled(
    client,
    db,
    project,
    completed_snapshot,
    owner_user,
):
    response = client.post(
        "/exports/requests",
        json={
            "project_id": project.id,
            "snapshot_id": completed_snapshot.id,
            "export_type": "image",
            "options": {},
        },
        headers=auth(owner_user),
    )

    assert response.status_code == 200

    entry = (
        db.query(JournalEntry)
        .filter_by(type="EXPORT_REQUESTED", actor_user_id=owner_user.id)
        .one()
    )

    assert entry is not None

