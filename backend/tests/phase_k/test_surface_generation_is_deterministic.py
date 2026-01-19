from app.services.surface_generator import generate_surface_from_curves

def test_surface_generation_is_deterministic(
    curve_set,
    params,
):
    s1 = generate_surface_from_curves(curves=curve_set, params=params)
    s2 = generate_surface_from_curves(curves=curve_set, params=params)

    assert s1.hash == s2.hash

