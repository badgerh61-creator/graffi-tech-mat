def test_validation_errors_are_display_only(
    ui_dispatcher,
    invalid_geometry_state,
):
    errors = ui_dispatcher.get_validation_errors()

    assert errors
    assert not ui_dispatcher.can_auto_fix()

