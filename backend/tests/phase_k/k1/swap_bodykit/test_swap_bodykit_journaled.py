def test_swap_bodykit_journal_entry_created(
    client,
    db,
    project,
    completed_snapshot,
    editor_user,
):
    response = client.post(
        "/mutations/decor/exterior/swap-bodykit",
        json={
            "project_id": project.id,
            "snapshot_base_id": completed_snapshot.id,
            "bodykit_id": "bk_1",
        },
        headers=auth(editor_user),
    )

    assert response.status_code == 200

    entries = db.execute(
        "SELECT * FROM journal_entries WHERE mutation_type = 'decor.exterior.swap-bodykit'"
    ).fetchall()

    assert len(entries) == 1

