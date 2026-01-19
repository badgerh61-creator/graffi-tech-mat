def serialize_snapshot_for_export(*, snapshot, format):
    """
    Deterministic serialization.
    No editor state.
    No timestamps.
    """
    return f"{snapshot.id}:{format}".encode()

