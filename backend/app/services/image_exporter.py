from app.models.export import ExportRecord
from app.services.jobs import enqueue_export_job
from app.services import audit


def create_image_export(*, db, snapshot, user, format, resolution):
    if snapshot.status != "completed":
        raise ValueError("Snapshot not exportable")

    export = ExportRecord(
        snapshot_id=snapshot.id,
        format=format,
        resolution=resolution,
        status="queued",
        created_by=user.id,
    )

    db.add(export)
    db.commit()
    db.refresh(export)

    enqueue_export_job(db=db, export_record=export)

    audit.log_event(
        db=db,
        user_id=user.id,
        action="snapshot.export.image",
        resource_type="snapshot",
        resource_id=snapshot.id,
        extra={
            "export_id": export.id,
            "format": format,
            "resolution": resolution,
        },
    )

    return export

