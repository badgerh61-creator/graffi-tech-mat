from app.services.distribution_capabilities import compute_distribution_capabilities
from app.services.distribution_revocation import revoke_distribution_request

def revoke_distribution(db, user, distribution_request):
    caps = compute_distribution_capabilities(
        user=user,
        project=distribution_request.export.project,
    )

    return revoke_distribution_request(
        db=db,
        user=user,
        distribution_request=distribution_request,
        capabilities=caps,
    )

