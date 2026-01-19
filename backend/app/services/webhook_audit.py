def record_webhook_attempt(*, db, webhook_id, event_type, success, response_code=None):
    # Append-only placeholder
    db.execute(
        "/* insert webhook audit record */"
    )
    db.commit()

