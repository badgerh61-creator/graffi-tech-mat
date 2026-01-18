from app.models.distribution_audit import DistributionAudit

def test_viewer_cannot_access_audit(
    client,
    completed_export,
    viewer_user,
):
    response = client.get(
        f"/distributions/audit?export_id={completed_export.id}",
        headers=auth(viewer_user),
    )

    assert response.status_code == 403

