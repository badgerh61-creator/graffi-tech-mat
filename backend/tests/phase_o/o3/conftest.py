from app.services.automation_job_executor import execute_job
from app.services.automation_job_audit import get_latest_job_log

import pytest

from app.models.automation_job import AutomationJob


@pytest.fixture
def automation_job(project):
    return AutomationJob(
        job_type="AUTO_EXPIRE_LINKS",
        policy="auto_expire_links",
        project_id=project.id,
        payload={},
    )


@pytest.fixture
def failing_job(project):
    return AutomationJob(
        job_type="AUTO_EXPIRE_LINKS",
        policy="auto_expire_links",
        project_id=project.id,
        payload={"force_fail": True},  # 👈 REQUIRED
        max_attempts=2,
    )


@pytest.fixture
def unknown_job(project):
    return AutomationJob(
        job_type="UNKNOWN_JOB_TYPE",
        policy="auto_expire_links",
        project_id=project.id,
        payload={},
    )


@pytest.fixture
def forbidden_job(project):
    return AutomationJob(
        job_type="AUTO_EXPIRE_LINKS",
        policy="auto_extend_link_lifetime",  # violates Phase N
        project_id=project.id,
        payload={},
    )


__all__ = [
    "execute_job",
    "get_latest_job_log",
]

