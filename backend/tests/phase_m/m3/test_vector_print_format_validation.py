import pytest
from app.services.vector_export import run_vector_export

def test_invalid_vector_format_rejected(
    db,
    completed_snapshot,
):
    with pytest.raises(ValueError):
        run_vector_export(
            db=db,
            snapshot=completed_snapshot,
            options={"format": "dxf"},
        )

