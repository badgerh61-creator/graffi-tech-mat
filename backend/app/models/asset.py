from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    ForeignKey,
    Text,
    Enum,
    JSON,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum

from app.db.base import Base


class AssetStatus(str, enum.Enum):
    created = "created"
    uploading = "uploading"
    uploaded = "uploaded"
    processing = "processing"
    ready = "ready"
    failed = "failed"


class Asset(Base):
    __tablename__ = "assets"

    id = Column(Integer, primary_key=True, index=True)

    filename = Column(String, nullable=False)
    content_type = Column(String, nullable=True)
    size = Column(Integer, nullable=True)

    s3_key = Column(String, unique=True, nullable=False)
    thumbnail_key = Column(String, nullable=True)

    # ✅ Phase 11.1 — SAFE name (NOT "metadata")
    asset_metadata = Column(JSON, nullable=True)

    status = Column(
        Enum(AssetStatus, name="asset_status"),
        nullable=False,
        default=AssetStatus.created,
    )

    status_updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    processing_error = Column(Text, nullable=True)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    model_id = Column(Integer, ForeignKey("models.id"), nullable=True)
    model = relationship("ModelRecord", back_populates="assets")

