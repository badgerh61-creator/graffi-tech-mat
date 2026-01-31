# backend/tests/phase_u_3/test_conflicted_draft_mutation_blocked.py

import pytest
from fastapi import HTTPException

from app.services.snapshot_fork import fork_snapshot


def test_conflicted_draft_mutation_blocked(
    db,
    completed_snapshot,
    editor_user,
):
    """
    Phase U.3 invariant:

    A conflicted or non-draft snapshot may NOT be forked.
    Forking is allowed ONLY from draft snapshots.
    """

    with pytest.raises(HTTPException) as exc:
        fork_snapshot(
            db=db,
            parent_snapshot=completed_snapshot,
            user=editor_user,
            reason="conflict-resolution",
        )

    assert exc.value.status_code == 409
