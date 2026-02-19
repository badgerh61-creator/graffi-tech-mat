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

    # -------------------------
    # Phase H.3 — reliability fields (ADDITIVE ONLY)
    # -------------------------

    # Idempotency: enqueue dedupe key (unique enforced via migration)
    idempotency_key = Column(String, nullable=True, index=True)

    # Execution timing & recovery
    started_at = Column(DateTime(timezone=True), nullable=True)
    finished_at = Column(DateTime(timezone=True), nullable=True)
    next_run_at = Column(DateTime(timezone=True), nullable=True)

    # Error visibility
    last_error = Column(String, nullable=True)

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
        # Existing code expects .status; keep mapping to canonical state
        return self.state

    @status.setter
    def status(self, value: str):
        self.state = value

    # -------------------------
    # Phase H.3 compatibility aliases
    # (maps new names -> existing Phase S fields)
    # -------------------------

    @property
    def attempts(self) -> int:
        # H.3 uses attempts; Phase S uses retry_count
        return int(self.retry_count or 0)

    @attempts.setter
    def attempts(self, value: int):
        self.retry_count = int(value or 0)

    @property
    def max_attempts(self) -> int:
        # H.3 uses max_attempts; Phase S uses max_retries
        return int(self.max_retries or 0)

    @max_attempts.setter
    def max_attempts(self, value: int):
        self.max_retries = int(value or 0)

