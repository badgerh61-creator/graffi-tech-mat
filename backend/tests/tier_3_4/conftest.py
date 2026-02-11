import pytest
from app.models.decor_preset import DecorPreset

@pytest.fixture
def decor_preset(db):
    preset = DecorPreset(
        name="Matatu Neon Pack",
        description="Kenyan urban neon interior",
        culture_pack="matatu_ke",
        category="interior",
        material_refs=[
            {"material_id": 1, "target_zone": "seat"}
        ],
        layout_refs=[],
        tags=["neon", "urban"],
        version=1,
    )

    db.add(preset)
    db.commit()
    db.refresh(preset)

    return preset

