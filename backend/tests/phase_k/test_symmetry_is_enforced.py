from app.services.surface_generator import generate_surface_from_curves
import pytest

def test_symmetry_is_enforced(
    asymmetric_curve_set,
):
    with pytest.raises(ValueError):
        generate_surface_from_curves(
            curves=asymmetric_curve_set,
            enforce_symmetry=True,
        )

