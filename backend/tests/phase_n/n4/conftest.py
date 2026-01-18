import pytest

from app.services.distribution_audit import record_distribution_event
from app.models.distribution_audit import DistributionAudit


# ----------------------------
# Fixture aliases (Phase N.4)
# ----------------------------

@pytest.fixture
def distribution_request(active_distribution_request, db, owner_user):
    """
    Phase N.4 observes distribution requests;
    it does not assume how they were created.
    """
    record_distribution_event(
        db=db,
        event_type="DISTRIBUTION_REQUESTED",
        export_id=active_distribution_request.export_id,
        distribution_request_id=active_distribution_request.id,
        actor_user_id=owner_user.id,
    )
    return active_distribution_request


@pytest.fixture
def signed_url(signed_url_distribution_request, admin_user, db):
    """
    Phase N.4 does not persist a SignedURL model.
    We assert audit side-effects instead.
    """
    record_distribution_event(
        db=db,
        event_type="SIGNED_URL_CREATED",
        export_id=signed_url_distribution_request.export_id,
        distribution_request_id=signed_url_distribution_request.id,
        actor_user_id=admin_user.id,
    )
    return signed_url_distribution_request


@pytest.fixture
def audit_record(db, completed_export, owner_user):
    """
    Explicit audit record for immutability testing.
    """
    return record_distribution_event(
        db=db,
        event_type="DISTRIBUTION_REQUESTED",
        export_id=completed_export.id,
        actor_user_id=owner_user.id,
    )

