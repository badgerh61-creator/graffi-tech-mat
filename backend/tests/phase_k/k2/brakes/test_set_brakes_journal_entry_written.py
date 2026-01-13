def test_brakes_journal_written(client, admin_user, completed_snapshot, db):
    auth(admin_user)

    res = client.post(
        "/mutations/tuning/set-brakes",
        json={
            "project_id": completed_snapshot.project_id,
            "snapshot_base_id": completed_snapshot.id,
            "preset_id": "sport",
        },
    )

    rows = db.execute(
        "SELECT * FROM journal_entries WHERE mutation_type = 'tuning.set-brakes'"
    ).fetchall()

    assert len(rows) == 1

