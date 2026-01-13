def test_brakes_requires_can_tune(
    client, editor_user_without_tuning_capability, completed_snapshot
):
    auth(editor_user_without_tuning_capability)

    res = client.post(
        "/mutations/tuning/set-brakes",
        json={
            "project_id": completed_snapshot.project_id,
            "snapshot_base_id": completed_snapshot.id,
            "preset_id": "sport",
        },
    )

    assert res.status_code == 403

