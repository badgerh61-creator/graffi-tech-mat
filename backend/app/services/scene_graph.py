# backend/app/services/scene_graph.py

from typing import List, Optional


class SceneGraphView:
    """
    READ-ONLY scene graph adapter.

    Phase 5 invariant:
    - No mutation
    - No DB access
    - Deterministic lookup only
    """

    def __init__(
        self,
        *,
        nodes: List[dict],
        panels: List[dict],
        curves: List[dict],
        reference_planes: List[dict],
    ):
        # 🔑 IMPORTANT:
        # Normalize ALL IDs to strings at the projection boundary.
        # Tests + frontend always use string IDs.
        self._nodes = {str(n["id"]): n for n in nodes}
        self._panels = {str(p["id"]): p for p in panels}
        self._curves = {str(c["id"]): c for c in curves}
        self._reference_planes = {
            str(r["id"]): r for r in reference_planes
        }

    # -------------------------------------------------
    # Lookup helpers (Phase 5.2 contract)
    # -------------------------------------------------

    def get_node(self, node_id: str) -> Optional["TargetView"]:
        data = self._nodes.get(str(node_id))
        return TargetView(data) if data else None

    def get_panel(self, panel_id: str) -> Optional["TargetView"]:
        data = self._panels.get(str(panel_id))
        return TargetView(data) if data else None

    def get_curve(self, curve_id: str) -> Optional["TargetView"]:
        data = self._curves.get(str(curve_id))
        return TargetView(data) if data else None

    def get_reference_plane(self, ref_id: str) -> Optional["TargetView"]:
        data = self._reference_planes.get(str(ref_id))
        return TargetView(data) if data else None

    # -------------------------------------------------
    # Generic lookup (Phase 5.3 contract)
    # -------------------------------------------------

    def get_element_by_id(self, element_id: str) -> Optional["TargetView"]:
        """
        Resolve any scene graph element by ID, regardless of type.
        """

        element_id = str(element_id)

        data = (
            self._nodes.get(element_id)
            or self._panels.get(element_id)
            or self._curves.get(element_id)
            or self._reference_planes.get(element_id)
        )

        return TargetView(data) if data else None


class TargetView:
    """
    Lightweight read-only wrapper around a scene element.
    """

    def __init__(self, data: dict):
        self._data = data

    @property
    def id(self) -> str:
        return str(self._data["id"])

    @property
    def editable(self) -> bool:
        # Phase 5 rule:
        # completed snapshots never expose editable targets
        return bool(self._data.get("editable", True))

    @property
    def kind(self) -> str:
        return self._data.get("type", "unknown")

