def test_export_blocked_while_draft_exists(
    client,
    project_with_draft,
    editor_user,
):
    res = client.post(
        "/exports",
        json={"project_id": project_with_draft.id},
        headers=auth(editor_user),
    )

    assert res.status_code == 409

