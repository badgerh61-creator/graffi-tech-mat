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

    # 🔒 Canonical lifecycle field
    state = Column(String, nullable=False, default="CREATED")

    # 🧱 Phase S — stability fields
    retry_count = Column(Integer, nullable=False, default=0)
    max_retries = Column(Integer, nullable=False, default=3)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    # -------------------------
    # Compatibility layer (DO NOT REMOVE)
    # -------------------------

    @property
    def status(self):
        return self.state

    @status.setter
    def status(self, value: str):
        self.state = value

