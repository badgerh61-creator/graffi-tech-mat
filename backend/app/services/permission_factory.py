ROLE_CAPABILITIES = {
    "owner": {...},
    "editor": {...},
    "viewer": set(),
}


def assign_role(db, *, user_id, project_id, role: str):
    caps = ROLE_CAPABILITIES[role]

    for cap in caps:
        db.add(
            ModelPermission(
                user_id=user_id,
                project_id=project_id,
                capability=cap,
            )
        )

