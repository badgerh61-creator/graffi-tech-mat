from app.models.distribution_audit import DistributionAudit

def test_signed_url_creation_audited(
    db,
    signed_url,
    admin_user,
):
    record = (
        db.query(DistributionAudit)
        .filter_by(
            event_type="SIGNED_URL_CREATED",
            distribution_request_id=signed_url.id,
        )
        .one()
    )

    assert record.actor_user_id == admin_user.id

