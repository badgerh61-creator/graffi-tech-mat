from app.services.signed_url_service import create_signed_url

def test_distribution_metrics_emitted(
    metrics_collector,
    distribution_request,
    db,
):

    create_signed_url(
        db=db,
        distribution_request=distribution_request,
        expires_in_hours=1,
    )

    assert metrics_collector.count("distribution.signed_url.created.count") == 1

