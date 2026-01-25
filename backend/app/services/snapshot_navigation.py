from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models.rendered_snapshot import RenderedSnapshot


# =====================================================
# Phase 5.5 — Undo
# =====================================================

def undo_snapshot(*, db: Session, snapshot: RenderedSnapshot, user):
    if user.role not in ("editor", "owner", "admin"):
        raise HTTPException(403, "Insufficient permissions")

    if snapshot.parent_snapshot_id is None:
        raise HTTPException(409, "No parent snapshot to undo to")

    parent = (
        db.query(RenderedSnapshot)
        .filter(RenderedSnapshot.id == snapshot.parent_snapshot_id)
        .first()
    )

    if not parent:
        raise HTTPException(409, "Parent snapshot missing")

    return parent


# =====================================================
# Phase 5.5 — Redo
# =====================================================

def redo_snapshot(*, db: Session, snapshot: RenderedSnapshot, user):
    if user.role not in ("editor", "owner", "admin"):
        raise HTTPException(403, "Insufficient permissions")

    child = (
        db.query(RenderedSnapshot)
        .filter(RenderedSnapshot.parent_snapshot_id == snapshot.id)
        .order_by(RenderedSnapshot.created_at.asc())
        .first()
    )

    if not child:
        raise HTTPException(409, "No child snapshot to redo to")

    return child

