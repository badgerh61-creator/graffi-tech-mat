from app.models.panel import Panel


def segment_surface(*, surface, bounds, label=None):
    """
    Phase K panel segmentation.

    Non-destructive by contract:
    - Does NOT modify the surface
    - Only references surface.id
    """

    return Panel(
        surface=surface,
        bounds=bounds,
        label=label,
    )

