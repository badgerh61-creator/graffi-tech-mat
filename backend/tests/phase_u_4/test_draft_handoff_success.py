import pytest

import app.services.presence_service as presence_service
from app.kernel import handoff_draft_ownership


def test_draft_handoff_success(
    db,
    locked_draft_snapshot,
    owner_user,
    editor_user,
):
    presence_service.mark_user_present(editor_user)

    result = handoff_draft_ownership(
        db=db,
        snapshot=locked_draft_snapshot,
        from_user=owner_user,
        to_user=editor_user,
    )

    assert result.user_id == editor_user.id

