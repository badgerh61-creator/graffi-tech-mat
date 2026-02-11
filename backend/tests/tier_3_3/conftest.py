import pytest
from app.models.material import Material

@pytest.fixture
def material_record(db):
    material = Material(
        name="Test Metal",
        category="metal",
        pbr_properties={
            "baseColor": "#aaaaaa",
            "roughness": 0.5,
            "metalness": 1.0,
            "normalMap": None,
            "emissive": None,
        },
        version=1,
        tags=["test"],
    )

    db.add(material)
    db.commit()
    db.refresh(material)

    return material

