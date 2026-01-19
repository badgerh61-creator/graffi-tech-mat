from app.services.surface_generator import generate_surface_from_curves

def test_param_slider_regenerates_surface(
    curve_set,
):
    surface1 = generate_surface_from_curves(
        curves=curve_set,
        params={"length": 4.2},
    )

    surface2 = generate_surface_from_curves(
        curves=curve_set,
        params={"length": 4.8},
    )

    assert surface1.hash != surface2.hash

