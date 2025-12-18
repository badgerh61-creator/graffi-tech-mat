from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.base import Base

class ModelRecord(Base):
    __tablename__ = "models"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

    asset_id = Column(Integer, ForeignKey("assets.id", ondelete="CASCADE"))
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))

    created_at = Column(DateTime, default=datetime.utcnow)

    asset = relationship("Asset", back_populates="models")
    owner = relationship("User", back_populates="models")
    patches = relationship("PatchRegistry", back_populates="model", cascade="all, delete")

