class AuthorizationError(Exception):
    pass


def require_capability(*, db, user_id, project_id, capability: str):
    exists = db.execute(
        """
        SELECT 1
        FROM model_permissions
        WHERE user_id = :user_id
          AND project_id = :project_id
          AND capability = :capability
        """,
        {
            "user_id": user_id,
            "project_id": project_id,
            "capability": capability,
        },
    ).first()

    if not exists:
        raise AuthorizationError()

