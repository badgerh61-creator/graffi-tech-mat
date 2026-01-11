def test_set_suspension_journal_entry_written(
    client,
    db,
    project,
    completed_snapshot,
    editor_user,
):
    response = client.post(
        "/mutations/tuning/set-suspension",
        json={
            "project_id": project.id,
            "snapshot_base_id": completed_snapshot.id,
            "preset_id": "sport_low",
        },
        headers=auth(editor_user),
    )

    assert response.status_code == 200

    entries = db.execute(
        "SELECT * FROM journal_entries WHERE mutation_type = 'tuning.set-suspension'"
    ).fetchall()

    assert len(entries) == 1

