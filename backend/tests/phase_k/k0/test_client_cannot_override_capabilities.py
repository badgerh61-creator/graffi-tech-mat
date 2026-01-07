def test_client_cannot_override_capabilities(
    request,
    client,
    project,
    editor_user,
):
    # 🔑 THIS LINE
    request.node.user = editor_user

    response = client.get(
        f"/workspaces/{project.id}?canDecorateExterior=true",
        headers=auth(editor_user),
    )

    caps = response.json()["capabilities"]

    assert caps["canDecorateExterior"] is True
    assert caps["canDecorateInterior"] is True
    assert caps["canTuneParameters"] is True
    assert caps["canModifyBody"] is False
    assert caps["canOverrideValidation"] is False

