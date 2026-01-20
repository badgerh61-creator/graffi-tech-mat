def test_panel_segmentation_from_ui(
    ui_dispatcher,
):
    ui_dispatcher.segment_panel(
        surface_id="surface-1",
        bounds="door",
    )

    command = ui_dispatcher.last_command()
    assert command["command"] == "SEGMENT_PANEL"

