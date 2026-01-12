def test_set_wheels_journal_entry_written(
    client,
    db,
    project,
    completed_snapshot,
    editor_user,
):
    response = client.post(
        "/mutations/tuning/set-wheels",
        json={
            "project_id": project.id,
            "snapshot_base_id": completed_snapshot.id,
            "diameter": 19,
            "width": 9.5,
            "offset": 35,
        },
        headers=auth(editor_user),
    )

    assert response.status_code == 200

    entries = db.execute(
        "SELECT * FROM journal_entries WHERE mutation_type = 'tuning.set-wheels'"
    ).fetchall()

    assert len(entries) == 1

