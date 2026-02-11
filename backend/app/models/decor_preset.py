from sqlalchemy import Column, Integer, String, JSON, DateTime
from sqlalchemy.sql import func
from app.db.base import Base

class DecorPreset(Base):
    __tablename__ = "decor_presets"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)

    culture_pack = Column(String, nullable=False)
    category = Column(String, nullable=False)  # interior | exterior | full

    material_refs = Column(JSON, nullable=False)
    layout_refs = Column(JSON, nullable=True)

    tags = Column(JSON, nullable=True)

    version = Column(Integer, nullable=False, default=1)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

