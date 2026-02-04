# backend/app/services/mode_resolver.py

from app.studio.modes import StudioMode


def resolve_mode(*, snapshot, user, station):

    if snapshot is None:
        return StudioMode.read_only

    if snapshot.status == "completed":
        return StudioMode.read_only

    if station == "validation":
        return StudioMode.review

    return StudioMode.editing

