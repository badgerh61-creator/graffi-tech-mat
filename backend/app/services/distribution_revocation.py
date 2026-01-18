from app.services.distribution_audit import record_distribution_event


def revoke_distribution_request(*, db, user, distribution_request, capabilities):
    if not capabilities["canRevokeAccess"]:
        raise PermissionError("Revocation not permitted")

    if distribution_request.revoked_at:
        raise RuntimeError("Already revoked")

    # 1️⃣ Revoke the request
    distribution_request.revoke()

    # 2️⃣ Revoke all signed URLs
    for url in getattr(distribution_request, "signed_urls", []):
        url.revoke()

    # 3️⃣ 🔒 AUDIT (MANDATORY FOR PHASE N.4)
    record_distribution_event(
        db=db,
        event_type="DISTRIBUTION_REVOKED",
        export_id=distribution_request.export_id,
        distribution_request_id=distribution_request.id,
        actor_user_id=user.id,
        project_id=distribution_request.export.project_id,
    )

    # 4️⃣ Persist
    db.commit()

    return {
        "status": "revoked",
        "revoked_at": distribution_request.revoked_at.isoformat(),
    }

