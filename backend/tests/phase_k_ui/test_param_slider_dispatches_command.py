def test_param_slider_dispatches_command(
    ui_dispatcher,
):
    ui_dispatcher.set_param("length", 4.5)

    command = ui_dispatcher.last_command()

    assert command["command"] == "SET_PARAM"
    assert command["param"] == "length"
    assert command["value"] == 4.5

