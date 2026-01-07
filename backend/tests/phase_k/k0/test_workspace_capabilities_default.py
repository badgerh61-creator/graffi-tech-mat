def test_workspace_has_no_write_capabilities_by_default(
    request,
    client,
    project,
    viewer_user,
):
   
    request.node.user = viewer_user

    response = client.get(
        f"/workspaces/{project.id}",
        headers=auth(viewer_user),
    )

    caps = response.json()["capabilities"]

    assert caps["canDecorateExterior"] is False
    assert caps["canDecorateInterior"] is False
    assert caps["canTuneParameters"] is False
    assert caps["canModifyBody"] is False
    assert caps["canOverrideValidation"] is False

