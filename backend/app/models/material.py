from sqlalchemy import Column, Integer, String, JSON, DateTime
from sqlalchemy.sql import func
from app.db.base import Base

class Material(Base):
    __tablename__ = "materials"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    category = Column(String, nullable=False)
    pbr_properties = Column(JSON, nullable=False)
    version = Column(Integer, nullable=False, default=1)
    tags = Column(JSON, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

