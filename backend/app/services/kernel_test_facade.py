"""
Kernel Test Facade

Authoritative entry points for stress / concurrency tests.
No logic lives here.
"""

# === Session Authority (U.1) ===
# 🔒 MUST use presence_sessions (authoritative kernel)
from app.services.presence_sessions import (
    start_session,
    require_active_session,
)

# === Draft Ownership (U.2) ===
from app.services.draft_ownership import (
    acquire_draft_lock,
    release_draft_lock,
    is_draft_owner,
)

# === Ownership Handoff (U.4) ===
from app.services.ownership_handoff import (
    handoff_draft_ownership,
)

# === Tool Execution (T + 5.x) ===
from app.services.tool_executor import (
    execute_tool,
)

# === Read Views (U.5) ===
from app.services.read_view_service import (
    open_read_view,
    has_active_read_view,
)

# === Conflict Detection (U.3) ===
from app.services.conflict_guard import (
    detect_conflict_or_raise,
)

# === Audit (P) ===
from app.services.audit import (
    get_audit_events,
)

