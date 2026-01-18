import pytest
from app.models.distribution_audit import DistributionAudit

def test_audit_record_cannot_be_modified(
    db,
    audit_record,
):
    audit_record.event_type = "HACKED"

    with pytest.raises(Exception):
        db.commit()

