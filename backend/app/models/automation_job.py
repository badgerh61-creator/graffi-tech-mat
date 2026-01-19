import uuid
from datetime import datetime


class AutomationJob:
    def __init__(
        self,
        job_type,
        policy,
        project_id,
        payload,
        max_attempts=3,
    ):
        # 🔑 REQUIRED for Phase O.3
        self.id = str(uuid.uuid4())

        self.job_type = job_type
        self.policy = policy
        self.project_id = project_id
        self.payload = payload

        self.status = "pending"
        self.attempt = 0
        self.max_attempts = max_attempts
        self.last_error = None

        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()

