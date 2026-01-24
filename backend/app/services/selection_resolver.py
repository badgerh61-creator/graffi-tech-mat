# backend/app/services/selection_resolver.py

from app.services.scene_graph import SceneGraphView


def resolve_selection(*, snapshot, selection_type, selection_id):
    """
    Phase 5.2 — Selection & Target Resolution

    Rules:
    - Only draft snapshots are editable
    - Selection must exist in scene graph
    - Target must be editable
    """

    scene = snapshot.scene_graph

    if selection_type == "node":
        target = scene.get_node(selection_id)
    elif selection_type == "panel":
        target = scene.get_panel(selection_id)
    elif selection_type == "curve":
        target = scene.get_curve(selection_id)
    elif selection_type == "reference_plane":
        target = scene.get_reference_plane(selection_id)
    else:
        raise ValueError("Invalid selection type")

    # 🔒 Phase 5.2 invariant:
    # Selection lookup failure → 404
    if target is None:
        raise KeyError("Selection not found")

    # 🔒 Phase 5.2 invariant:
    # Completed snapshots never expose editable targets
    if not snapshot.is_draft:
        raise PermissionError("Snapshot not editable")

    # 🔒 Phase 5.2 invariant:
    # Target-level editability
    if not target.editable:
        raise PermissionError("Target not editable")

    return {
        "target_id": target.id,
        "target_type": selection_type,
        "editable": True,
    }

