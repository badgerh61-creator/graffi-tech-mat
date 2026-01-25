from sqlalchemy import Column, Integer, String, ForeignKey, JSON
from app.db.base import Base


class CurveConstraint(Base):
    __tablename__ = "curve_constraints"  # ✅ UNIQUE TABLE

    id = Column(Integer, primary_key=True)

    snapshot_id = Column(
        Integer,
        ForeignKey("rendered_snapshots.id", ondelete="CASCADE"),
        nullable=False,
    )

    curve_id = Column(
        Integer,
        ForeignKey("curves.id", ondelete="CASCADE"),
        nullable=False,
    )

    type = Column(String, nullable=False)
    reference = Column(String, nullable=True)
    params = Column(JSON, nullable=False)

