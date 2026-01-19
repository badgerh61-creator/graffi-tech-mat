from app.utils.ids import generate_id


class Panel:
    """
    Level-2 Panel model.

    Panels are logical segmentations of a Surface.
    They MUST NOT modify surface geometry.
    """

    def __init__(self, *, surface, bounds, label=None):
        if surface is None:
            raise ValueError("Panel requires a surface")

        if not hasattr(surface, "id"):
            raise ValueError("Surface must have an id")

        self.id = generate_id()

        # 🔒 Non-destructive reference
        self.surface_id = surface.id

        # Logical metadata only
        self.bounds = bounds
        self.label = label or "panel"

