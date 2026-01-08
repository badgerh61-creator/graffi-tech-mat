from app.models.mutation_journal import MutationJournal


def test_decor_mutation_writes_journal(
    request,
    client,
    db,
    project,
    completed_snapshot,
    editor_user,
):
    request.node.user = editor_user  # ✅ REQUIRED

    response = client.post(
        "/mutations/decor/exterior/apply-decal",
        json={
            "project_id": project.id,
            "snapshot_base_id": completed_snapshot.id,
            "decal_id": "test_decal",
            "target": {
                "panel": "door_left",
                "uv_transform": {
                    "x": 0.1,
                    "y": 0.2,
                    "scale": 1.0,
                    "rotation": 0,
                }
            },
        },
    )

    snapshot_id = response.json()["snapshot_id"]

    entry = (
        db.query(MutationJournal)
        .filter_by(
            intent_type="decor.exterior.apply-decal",
            target_type="snapshot",
            target_id=snapshot_id,
        )
        .one()
    )

    assert entry.issued_by_user_id == editor_user.id

