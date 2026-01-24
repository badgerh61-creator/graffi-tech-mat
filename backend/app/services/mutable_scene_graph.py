class MutableSceneGraph:
    """
    WRITE-capable scene graph.

    Phase 5 invariant:
    - Mutates in-memory state only
    - No DB access
    - Deterministic output
    """

    def __init__(self, *, body_state: dict):
        # Operate directly on canonical state
        self._state = body_state or {}

        self._nodes = self._index("nodes")
        self._panels = self._index("panels")
        self._curves = self._index("curves")
        self._reference_planes = self._index("reference_planes")

    def _index(self, key: str):
        items = self._state.get(key, [])
        return {str(i["id"]): i for i in items}

    # -------------------------------------------------
    # Target resolution (mirrors SceneGraphView)
    # -------------------------------------------------

    def get_element(self, element_id: str):
        element_id = str(element_id)

        return (
            self._nodes.get(element_id)
            or self._panels.get(element_id)
            or self._curves.get(element_id)
            or self._reference_planes.get(element_id)
        )

    # -------------------------------------------------
    # Transform execution (Phase 5.4)
    # -------------------------------------------------

    def apply_transform(self, *, target_id: str, operation: str, params: dict):
        target = self.get_element(target_id)

        if not target:
            return  # safe no-op

        transform = target.setdefault("transform", {
            "x": 0, "y": 0, "z": 0,
            "rx": 0, "ry": 0, "rz": 0,
            "sx": 1, "sy": 1, "sz": 1,
        })

        if operation == "translate":
            for axis in ("x", "y", "z"):
                if axis in params:
                    transform[axis] += params[axis]

        elif operation == "rotate":
            for axis in ("x", "y", "z"):
                key = f"r{axis}"
                if axis in params:
                    transform[key] += params[axis]

        elif operation == "scale":
            for axis in ("x", "y", "z"):
                key = f"s{axis}"
                if axis in params:
                    transform[key] *= params[axis]

    # -------------------------------------------------
    # Serialization
    # -------------------------------------------------

    def serialize(self) -> dict:
        return self._state

