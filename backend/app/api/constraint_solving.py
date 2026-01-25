from fastapi import HTTPException
from app.services.constraint_solver import solve_constraints

def solve_constraints_endpoint(db, snapshot, user):
    if user.role not in ("editor", "owner", "admin"):
        raise HTTPException(403)

    return solve_constraints(
        db=db,
        snapshot=snapshot,
        user=user,
    )

