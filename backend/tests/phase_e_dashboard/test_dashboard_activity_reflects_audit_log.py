def test_dashboard_activity_reflects_audit_log(
    client,
    editor_user,
):
    response = client.get(
        "/dashboard/activity",
        headers=auth(editor_user),
    )

    items = response.json()
    assert all("action" in i for i in items)

