from datetime import datetime
from sqlalchemy import Column, Integer, String, JSON, DateTime

from app.db.base import Base


class AutomationJob(Base):
    __tablename__ = "automation_jobs"

    id = Column(Integer, primary_key=True)

    job_type = Column(String, nullable=False)
    policy = Column(String, nullable=False)
    project_id = Column(Integer, nullable=False)

    payload = Column(JSON, nullable=False)

    status = Column(String, nullable=False, default="pending")
    attempt = Column(Integer, nullable=False, default=0)
    max_attempts = Column(Integer, nullable=False, default=3)

    last_error = Column(String, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    def __init__(
        self,
        job_type,
        policy,
        project_id,
        payload,
        max_attempts=None,
    ):
        self.job_type = job_type
        self.policy = policy
        self.project_id = project_id
        self.payload = payload

        # 🔒 In-memory defaults (required for Phase O.3)
        self.status = "pending"
        self.attempt = 0
        self.max_attempts = max_attempts if max_attempts is not None else 3

