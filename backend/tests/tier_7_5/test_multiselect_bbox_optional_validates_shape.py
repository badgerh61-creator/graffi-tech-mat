from app.services.selection_payload import normalize_multiselect_payload

def test_multiselect_bbox_optional_validates_shape():
    out = normalize_multiselect_payload(
        payload={
            "selected_target_ids": ["a", "b"],
            "selection_bbox": {
                "min": {"x": 0, "y": 0, "z": 0},
                "max": {"x": 10, "y": 5, "z": 2},
            },
        }
    )
    assert out["pivot_mode"] == "bbox_center"
    assert out["selection_bbox"]["max"]["x"] == 10.0
