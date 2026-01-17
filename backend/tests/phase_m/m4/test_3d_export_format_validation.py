from app.services.three_d_export import run_3d_export

import pytest

def test_invalid_3d_format_rejected(
    db,
    completed_snapshot,
):
    with pytest.raises(ValueError):
        run_3d_export(
            db=db,
            snapshot=completed_snapshot,
            options={"format": "fbx"},
        )

