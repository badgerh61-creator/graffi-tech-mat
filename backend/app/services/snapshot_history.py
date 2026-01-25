from fastapi import HTTPException

def undo_snapshot(*, snapshot):
    if not snapshot.parent_snapshot:
        raise HTTPException(409, "No parent snapshot")

    return snapshot.parent_snapshot


def redo_snapshot(*, snapshot):
    if not snapshot.child_snapshots:
        raise HTTPException(409, "No child snapshot")

    # deterministic: latest child
    return snapshot.child_snapshots[-1]

