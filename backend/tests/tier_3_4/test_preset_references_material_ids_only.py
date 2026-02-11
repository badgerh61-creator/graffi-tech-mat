def test_preset_references_material_ids_only(decor_preset):
    for ref in decor_preset.material_refs:
        assert "material_id" in ref
        assert isinstance(ref["material_id"], int)

