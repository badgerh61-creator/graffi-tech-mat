def test_ai_editor_can_request_proposal(
    assistant_service,
    editor_user,
    snapshot,
):
    response = assistant_service.handle_request(
        user=editor_user,
        snapshot=snapshot,
        mode="proposal",
        prompt="Suggest curvature fix",
    )

    assert response["mode"] == "proposal"
    assert "proposals" in response
