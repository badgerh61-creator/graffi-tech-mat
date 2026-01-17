import pytest
from app.services.print_export import run_print_export

def test_print_export_missing_dpi_rejected(
    db,
    completed_snapshot,
):
    with pytest.raises(ValueError):
        run_print_export(
            db=db,
            snapshot=completed_snapshot,
            options={
                "format": "tiff",
                "units": "mm",
                "color_profile": "CMYK",
            },
        )

