def test_editor_capabilities_are_limited(
    request,
    client,
    project,
    editor_user,
):
   
    request.node.user = editor_user

    response = client.get(
        f"/workspaces/{project.id}",
        headers=auth(editor_user),
    )

    caps = response.json()["capabilities"]

    assert caps["canDecorateExterior"] is True
    assert caps["canDecorateInterior"] is True
    assert caps["canTuneParameters"] is True
    assert caps["canModifyBody"] is False
    assert caps["canOverrideValidation"] is False


def test_admin_has_all_capabilities(
    client,
    project,
    admin_user,
):
    response = client.get(
        f"/workspaces/{project.id}",
        headers=auth(admin_user),
    )

    caps = response.json()["capabilities"]

    assert all(value is True for value in caps.values())

