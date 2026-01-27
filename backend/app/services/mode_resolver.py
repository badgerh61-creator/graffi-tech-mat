from app.studio.modes import StudioMode

def resolve_mode(*, snapshot, user, station):
    """
    Authoritatively resolve current studio mode.
    """

    if snapshot.status == "completed":
        return StudioMode.read_only

    if station == "validation":
        return StudioMode.review

    return StudioMode.editing

