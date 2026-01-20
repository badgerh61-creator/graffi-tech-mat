import pytest
from datetime import datetime, timedelta
from app.compliance.compliance_record import ComplianceRecord
from app.compliance.retention_engine import RetentionEngine

@pytest.fixture
def retention_engine():
    return RetentionEngine()

@pytest.fixture
def audit_record():
    return ComplianceRecord(
        id="audit-1",
        record_type="audit",
        created_at=datetime.utcnow() - timedelta(days=400),
    )

@pytest.fixture
def recent_snapshot():
    return ComplianceRecord(
        id="snapshot-recent",
        record_type="snapshot",
        created_at=datetime.utcnow() - timedelta(days=5),
    )

@pytest.fixture
def old_snapshot():
    return ComplianceRecord(
        id="snapshot-old",
        record_type="snapshot",
        created_at=datetime.utcnow() - timedelta(days=500),
    )

@pytest.fixture
def snapshot_under_legal_hold():
    return ComplianceRecord(
        id="snapshot-hold",
        record_type="snapshot",
        created_at=datetime.utcnow() - timedelta(days=500),
        legal_hold=True,
    )

