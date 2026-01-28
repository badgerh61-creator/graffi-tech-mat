from sqlalchemy import Column, Integer, DateTime
from app.db.base import Base


class StudioSession(Base):
    """
    Phase U.1 — Execution authority envelope.
    Required for all kernel actions.
    """

    __tablename__ = "studio_sessions"

    id = Column(Integer, primary_key=True)

    user_id = Column(Integer, nullable=False, index=True)
    project_id = Column(Integer, nullable=False, index=True)

    # Optional: for snapshot-scoped authority (Phase U.2+)
    snapshot_id = Column(Integer, nullable=True)

    expires_at = Column(DateTime(timezone=True), nullable=False)

