def test_set_material_journal_entry_created(
    client,
    db,
    project,
    completed_snapshot,
    editor_user,
):
    response = client.post(
        "/mutations/decor/exterior/set-material",
        json={
            "project_id": project.id,
            "snapshot_base_id": completed_snapshot.id,
            "panel": "door_left",
            "material": {
                "material_id": "mat_1",
                "parameters": {
                    "color": "#FFFFFF",
                    "finish": "gloss",
                },
            },
        },
        headers=auth(editor_user),
    )

    assert response.status_code == 200
    new_snapshot_id = response.json()["snapshot_id"]

    entries = db.execute(
        """
        SELECT *
        FROM journal_entries
        WHERE mutation_type = 'decor.exterior.set-material'
          AND snapshot_after = :snapshot_id
        """,
        {"snapshot_id": new_snapshot_id},
    ).fetchall()

    assert len(entries) == 1

