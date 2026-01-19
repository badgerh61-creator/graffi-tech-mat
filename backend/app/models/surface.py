from app.utils.ids import generate_id
from app.utils.surface_hash import compute_surface_hash


class Surface:
    """
    Level-2 derived surface.

    Identity (id) is instance-specific.
    Equality is geometry-specific (hash-based).
    """

    def __init__(self, *, source_curves, params, method):
        self.id = generate_id()
        self.source_curves = list(source_curves)
        self.params = dict(params or {})
        self.method = method
        self.hash = compute_surface_hash(
            curves=self.source_curves,
            params=self.params,
            method=self.method,
        )

    def __eq__(self, other):
        """
        Deterministic equality.

        Two surfaces are equal if they represent
        the same derived geometry, regardless of identity.
        """
        if not isinstance(other, Surface):
            return False

        return self.hash == other.hash

    def __repr__(self):
        return f"<Surface hash={self.hash[:8]} id={self.id}>"

