from app.services.panel_segmentation import segment_surface

def test_panel_segmentation_is_non_destructive(
    surface,
):
    panel = segment_surface(surface=surface, bounds="door")

    assert panel.surface_id == surface.id

