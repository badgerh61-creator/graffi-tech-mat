from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.session import Base


class Asset(Base):
    __tablename__ = "assets"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, nullable=False)
    content_type = Column(String, nullable=True)
    size = Column(Integer, nullable=True)
    s3_key = Column(String, unique=True, nullable=False)

    thumbnail_key = Column(String, nullable=True)

    # 🔒 Processing state (Phase 4.1)
    processed = Column(Boolean, default=False, nullable=False)
    processed_at = Column(DateTime(timezone=True), nullable=True)
    processing_error = Column(Text, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    model_id = Column(Integer, ForeignKey("models.id"), nullable=True)
    model = relationship("ModelRecord", back_populates="assets")

