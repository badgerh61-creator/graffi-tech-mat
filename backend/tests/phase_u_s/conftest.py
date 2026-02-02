import pytest


@pytest.fixture
def user_a(owner_user):
    return owner_user


@pytest.fixture
def user_b(editor_user):
    return editor_user


@pytest.fixture
def conflicted_draft_snapshot(draft_snapshot):
    # For now, reuse a normal draft snapshot.
    # Conflict semantics are injected by guards, not data shape.
    return draft_snapshot

