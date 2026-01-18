from app.models.distribution_audit import DistributionAudit

def test_distribution_request_is_audited(
    db,
    distribution_request,
    owner_user,
):
    record = (
        db.query(DistributionAudit)
        .filter_by(
            event_type="DISTRIBUTION_REQUESTED",
            distribution_request_id=distribution_request.id,
        )
        .one()
    )

    assert record.actor_user_id == owner_user.id

