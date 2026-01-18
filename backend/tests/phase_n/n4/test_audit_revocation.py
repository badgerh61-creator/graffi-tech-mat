from app.models.distribution_audit import DistributionAudit

def test_revocation_is_audited(
    db,
    revoked_distribution_request,
    admin_user,
):
    record = (
        db.query(DistributionAudit)
        .filter_by(
            event_type="DISTRIBUTION_REVOKED",
            distribution_request_id=revoked_distribution_request.id,
        )
        .one()
    )

    assert record is not None

