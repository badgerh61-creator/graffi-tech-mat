from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.db.base import Base


class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)
    mutation_id = Column(Integer, ForeignKey("mutation_journal.id"), nullable=False)

    job_type = Column(String, nullable=False)
    target_type = Column(String, nullable=False)
    target_id = Column(Integer, nullable=False)

    state = Column(String, nullable=False, default="CREATED")

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
    DateTime(timezone=True),
    server_default=func.now(),   # ✅ set on INSERT
    onupdate=func.now(),         # ✅ update on UPDATE
    nullable=False,
)


