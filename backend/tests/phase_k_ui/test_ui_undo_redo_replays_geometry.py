def test_ui_undo_redo_replays_geometry(
    ui_dispatcher,
    geometry_engine,
):
    ui_dispatcher.set_param("length", 4.6)
    h1 = geometry_engine.current_surface().hash

    ui_dispatcher.undo()
    ui_dispatcher.redo()
    h2 = geometry_engine.current_surface().hash

    assert h1 == h2

