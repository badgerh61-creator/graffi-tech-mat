from sqlalchemy import Column, Integer, String, DateTime, JSON
from sqlalchemy.sql import func
from app.db.base import Base


class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True)

    user_id = Column(Integer, nullable=True)

    action = Column(String, nullable=False)

    resource_type = Column(String, nullable=False)
    resource_id = Column(Integer, nullable=True)

    # ✅ MUST NOT be named "metadata"
    extra = Column(JSON, nullable=True)

    ip_address = Column(String, nullable=True)
    user_agent = Column(String, nullable=True)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

