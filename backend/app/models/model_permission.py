from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from app.db.base import Base

class ModelPermission(Base):
    __tablename__ = "model_permissions"

    id = Column(Integer, primary_key=True)
    model_id = Column(
        Integer,
        ForeignKey("models.id", ondelete="CASCADE"),
        nullable=False,
    )
    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )

    # viewer | editor
    role = Column(String, nullable=False, default="viewer")

    __table_args__ = (
        UniqueConstraint("model_id", "user_id", name="uq_model_user"),
    )

    user = relationship("User")
    model = relationship(
    "ModelRecord",
    back_populates="permissions",
    overlaps="permissions",
)


