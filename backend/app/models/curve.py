from sqlalchemy import Column, Integer, String, ForeignKey, JSON
from app.db.base import Base


class Curve(Base):
    __tablename__ = "curves"

    id = Column(Integer, primary_key=True)
    snapshot_id = Column(Integer, ForeignKey("rendered_snapshots.id"), nullable=False)

    type = Column(String, nullable=False)
    reference_plane_id = Column(String, nullable=False)

    params = Column(JSON, nullable=False)
    constraints = Column(JSON, nullable=False, default=list)

