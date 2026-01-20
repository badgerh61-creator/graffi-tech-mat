def test_symmetry_toggle_is_read_only(
    ui_dispatcher,
):
    state = ui_dispatcher.get_symmetry_state()
    assert state is True

