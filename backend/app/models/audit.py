# backend/app/models/audit.py

"""
Audit compatibility alias.

Provides a stable import path:
    from app.models.audit import AuditLog

Authoritative implementation lives in:
    app.models.audit_log.AuditLog
"""

from app.models.audit_log import AuditLog

__all__ = ["AuditLog"]

