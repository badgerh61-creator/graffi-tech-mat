import pytest
from app.services.image_export import run_image_export


def test_unsupported_format_rejected(
    db,
    completed_snapshot,
):
    with pytest.raises(ValueError):
        run_image_export(
            db=db,
            snapshot=completed_snapshot,
            options={"format": "gif"},
        )

