def compute_distribution_capabilities(*, user, project):
    # Archived projects are frozen
    if project.archived_at is not None:
        return {
            "canDistributeExports": False,
            "canCreatePublicLinks": False,
            "canRevokeAccess": False,
        }

    # Admin
    if user.role == "admin":
        return {
            "canDistributeExports": True,
            "canCreatePublicLinks": True,
            "canRevokeAccess": True,
        }

    # Owner
    if user.role == "owner":
        return {
            "canDistributeExports": True,
            "canCreatePublicLinks": False,
            "canRevokeAccess": True,
        }

    # Viewer / Editor
    return {
        "canDistributeExports": False,
        "canCreatePublicLinks": False,
        "canRevokeAccess": False,
    }

