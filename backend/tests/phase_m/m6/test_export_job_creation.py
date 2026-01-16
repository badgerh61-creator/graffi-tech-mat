from app.models.export_job import ExportJob

def test_job_created_from_export_request(
    client,
    db,
    project,
    completed_snapshot,
    owner_user,
):
    # create export request
    response = client.post(
        "/exports/requests",
        json={
            "project_id": project.id,
            "snapshot_id": completed_snapshot.id,
            "export_type": "image",
            "options": {},
        },
        headers=auth(owner_user),
    )

    export_request_id = response.json()["export_request_id"]

    job = (
        db.query(ExportJob)
        .filter_by(export_request_id=export_request_id)
        .one()
    )

    assert job.status == "requested"

