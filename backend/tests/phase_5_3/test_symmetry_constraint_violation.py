def test_symmetry_constraint_violation(
    client,
    draft_snapshot,
    editor_user,
):
    response = client.post(
        f"/projects/{draft_snapshot.project_id}/snapshots/{draft_snapshot.id}/validate-transform",
        json={
            "target_id": "door.front.left",
            "operation": "translate",
            "params": {"x": 0.3, "y": 0, "z": 0},
            "constraints": ["symmetry:vehicle_centerline"],
        },
        headers=auth(editor_user),
    )

    data = response.json()
    assert data["valid"] is False
    assert data["violations"][0]["constraint"] == "symmetry"

