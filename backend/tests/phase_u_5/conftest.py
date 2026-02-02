import pytest
from datetime import timedelta
from freezegun import freeze_time

from app.services.presence_sessions import start_session
from app.services.read_view_service import open_read_view
from app.services.read_view_guard import has_active_read_view
from app.services.draft_lock_service import acquire_draft_lock
from app.services.studio_kernel import execute_tool


# --- Service function fixtures ---

@pytest.fixture
def start_session_fn():
    return start_session


@pytest.fixture
def open_read_view_fn():
    return open_read_view


@pytest.fixture
def has_active_read_view_fn():
    return has_active_read_view


@pytest.fixture
def acquire_draft_lock_fn():
    return acquire_draft_lock


@pytest.fixture
def execute_tool_fn():
    return execute_tool
    

# --- Time control (REQUIRED for expiry tests) ---

@pytest.fixture
def advance_time():
    """
    Safe, re-entrant time control.
    Works even if another freezer is already active.
    """
    with freeze_time() as freezer:
        def _advance(*, seconds: int):
            freezer.tick(delta=timedelta(seconds=seconds))
        yield _advance

