def test_param_change_regenerates_surface(
    geometry_engine,
    curve_set,
):
    surface1 = geometry_engine.generate(curves=curve_set)

    geometry_engine.apply_command({
        "command": "SET_PARAM",
        "param": "length",
        "value": 4.9,
    })

    surface2 = geometry_engine.current_surface()

    assert surface1.hash != surface2.hash

