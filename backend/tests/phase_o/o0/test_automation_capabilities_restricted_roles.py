from app.services.automation_capabilities import compute_automation_capabilities


def test_viewer_cannot_enable_automation(
    project,
    viewer_user,
):
    caps = compute_automation_capabilities(
        user=viewer_user,
        project=project,
    )

    assert all(value is False for value in caps.values())


def test_editor_cannot_enable_automation(
    project,
    editor_user,
):
    caps = compute_automation_capabilities(
        user=editor_user,
        project=project,
    )

    assert all(value is False for value in caps.values())

