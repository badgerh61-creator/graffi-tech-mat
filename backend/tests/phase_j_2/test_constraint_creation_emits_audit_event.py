import pytest

from app.services.curve_constraints import add_curve_constraint
from app.models.audit_log import AuditLog


def test_constraint_creation_emits_audit_event(
    db,
    draft_snapshot,
    curve,
    editor_user,
):
    new_snapshot, constraint = add_curve_constraint(
        db=db,
        snapshot=draft_snapshot,
        curve=curve,
        user=editor_user,
        constraint_type="fixed_length",
        reference=None,
        params={"length": 120},
    )

    events = (
        db.query(AuditLog)
        .filter(
            AuditLog.action == "curve.constraint.add",
            AuditLog.resource_id == constraint.id,
        )
        .all()
    )

    assert len(events) == 1

