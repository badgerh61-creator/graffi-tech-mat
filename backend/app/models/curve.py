from sqlalchemy import Column, Integer, String, ForeignKey, JSON
from sqlalchemy.orm import synonym
from app.db.base import Base


class Curve(Base):
    __tablename__ = "curves"

    id = Column(Integer, primary_key=True)

    snapshot_id = Column(
        Integer,
        ForeignKey(
            "rendered_snapshots.id",
            ondelete="CASCADE",
            use_alter=True,
            name="fk_curves_snapshot_id",
        ),
        nullable=False,
    )

    # 🔒 CANONICAL COLUMN
    type = Column(String, nullable=False)

    # 🔁 COMPATIBILITY ALIAS (Phase J.2 fixtures)
    curve_type = synonym("type")

    reference_plane_id = Column(String, nullable=False)

    params = Column(JSON, nullable=False)

    constraints = Column(
        JSON,
        nullable=False,
        default=list,
    )

