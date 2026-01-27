def resolve_flow_state(snapshot):
    """
    Infer current flow state from snapshot lineage.
    """

    if snapshot.status == "completed":
        return "finalize"

    # Stub logic: derive from snapshot metadata / history
    # Default starting state
    return snapshot.last_flow_state or "start"

