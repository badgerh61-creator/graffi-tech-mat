from app.models.distribution_audit import DistributionAudit

def record_distribution_event(
    *,
    db,
    event_type,
    export_id,
    actor_user_id,
    distribution_request_id=None,
    project_id=None,
    metadata=None,
):
    record = DistributionAudit(
        event_type=event_type,
        export_id=export_id,
        distribution_request_id=distribution_request_id,
        project_id=project_id,
        actor_user_id=actor_user_id,
        metadata=metadata,
    )

    db.add(record)
    db.commit()
    return record

