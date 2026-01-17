def revoke_distribution_request(*, db, user, distribution_request, capabilities):
    if not capabilities["canRevokeAccess"]:
        raise PermissionError("Revocation not permitted")

    if distribution_request.revoked_at:
        raise RuntimeError("Already revoked")

    distribution_request.revoke()

    for url in getattr(distribution_request, "signed_urls", []):
        url.revoke()

    db.commit()

    return {
        "status": "revoked",
        "revoked_at": distribution_request.revoked_at.isoformat(),
    }

