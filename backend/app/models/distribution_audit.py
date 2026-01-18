from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, JSON, event
from app.db.base import Base


class DistributionAudit(Base):
    __tablename__ = "distribution_audits"

    id = Column(Integer, primary_key=True)

    event_type = Column(String, nullable=False)

    project_id = Column(Integer, nullable=True)
    export_id = Column(Integer, nullable=False)
    distribution_request_id = Column(Integer, nullable=True)

    actor_user_id = Column(Integer, nullable=False)

    # 🔒 FIX: metadata is reserved → use metadata_
    metadata_ = Column("metadata", JSON, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)


# 🔒 Immutability enforcement
@event.listens_for(DistributionAudit, "before_update")
def prevent_update(mapper, connection, target):
    raise Exception("Audit records are immutable")


@event.listens_for(DistributionAudit, "before_delete")
def prevent_delete(mapper, connection, target):
    raise Exception("Audit records are immutable")

