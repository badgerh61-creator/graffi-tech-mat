from datetime import datetime, timedelta
from app.compliance.retention_policies import (
    IMMUTABLE_RECORD_TYPES,
    DEFAULT_RETENTION,
)
from app.compliance.legal_hold import is_under_legal_hold
from app.observability.events import emit_event

class RetentionEngine:
    def is_purge_allowed(self, *, record):
        if record.type in IMMUTABLE_RECORD_TYPES:
            return False

        if is_under_legal_hold(record):
            return False

        policy = DEFAULT_RETENTION.get(record.type)
        if not policy:
            return False

        age = (datetime.utcnow() - record.created_at).days

        return age >= policy["max_days"]

    def purge(self, *, record):
        if not self.is_purge_allowed(record=record):
            return {"purged": False}

        # Stub: actual deletion deferred
        emit_event(
            event_type="RETENTION_PURGE",
            payload={
                "record_id": record.id,
                "record_type": record.type,
            },
        )

        return {
            "purged": True,
            "event_emitted": True,
        }

    def generate_report(self):
        return {
            "policies": DEFAULT_RETENTION,
            "legal_holds": [],
            "purges": [],
        }

