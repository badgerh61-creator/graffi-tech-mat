from fastapi import HTTPException

SUPPORTED_TARGETS = {"direct_download", "signed_url", "external_system"}


def create_distribution_request(*, db, user, export, target, options, capabilities):
    if not capabilities["canDistributeExports"]:
        raise HTTPException(status_code=403, detail="Distribution not permitted")

    if export.status != "completed":
        raise HTTPException(status_code=409, detail="Export not distributable")

    if target not in SUPPORTED_TARGETS:
        raise HTTPException(status_code=400, detail="Unsupported distribution target")

    if target == "signed_url" and not capabilities["canCreatePublicLinks"]:
        raise HTTPException(status_code=403, detail="Public links not permitted")

    from app.models.distribution_request import DistributionRequest

    req = DistributionRequest(
        export_id=export.id,
        target=target,
        options=options,
    )

    db.add(req)
    db.commit()
    db.refresh(req)
    return req

