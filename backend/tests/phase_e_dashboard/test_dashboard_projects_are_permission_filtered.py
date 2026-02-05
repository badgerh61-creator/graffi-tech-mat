def test_dashboard_projects_are_permission_filtered(
    client,
    viewer_user,
):
    response = client.get(
        "/dashboard/projects",
        headers=auth(viewer_user),
    )

    projects = response.json()
    assert all("project_id" in p for p in projects)

