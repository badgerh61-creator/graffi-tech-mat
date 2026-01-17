# backend/app/services/workspace_builder.py (extension)

from app.services.distribution_capabilities import compute_distribution_capabilities

def attach_distribution_capabilities(workspace, user, project):
    workspace["distribution_capabilities"] = compute_distribution_capabilities(
        user=user,
        project=project,
    )

