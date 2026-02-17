# backend/app/models/assistant_proposal.py
# =========================================
# Tier 4.5 — Assistant Proposal ORM
# Authoritative proposal record (no auto-apply)
# =========================================

from sqlalchemy import Column, Integer, String, JSON, ForeignKey
from sqlalchemy.orm import relationship

from app.db.base import Base


class AssistantProposal(Base):
    __tablename__ = "assistant_proposals"

    # ✅ FIX: autoincrement PK so sqlite + tests can insert rows
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)

    snapshot_id = Column(Integer, ForeignKey("rendered_snapshots.id"), nullable=False)

    # Phase T concepts
    station = Column(String, nullable=False)   # e.g. "geometry"
    tool = Column(String, nullable=False)      # e.g. "translate"
    payload = Column(JSON, nullable=False, default=dict)

    # Optional metadata
    rationale = Column(String, nullable=True)
    risk_level = Column(String, nullable=False, default="low")

    # Optional actor link (tests can set it; DB can allow NULL)
    created_by_user_id = Column(Integer, ForeignKey("users.id"), nullable=True)

    # relationships (safe, optional)
    snapshot = relationship("RenderedSnapshot", lazy="joined", viewonly=True)
