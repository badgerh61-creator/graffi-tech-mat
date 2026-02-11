# backend/app/services/session_guard.py

# session_guard.py

"""
Phase U Adapter — Session Guard

This module is intentionally thin.
It exists only for backward compatibility.

Authoritative session enforcement lives in:
app.services.presence_sessions
"""

from app.services.presence_sessions import require_active_session

__all__ = ["require_active_session"]
