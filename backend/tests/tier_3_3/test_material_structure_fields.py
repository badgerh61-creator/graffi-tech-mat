def test_material_structure_fields(db, material_record):
    assert material_record.name is not None
    assert material_record.category in (
        "fabric",
        "metal",
        "paint",
        "leather",
        "glass",
    )

