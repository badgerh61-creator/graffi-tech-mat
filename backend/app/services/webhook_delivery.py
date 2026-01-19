import hmac
import hashlib
import json
from datetime import datetime

def sign_payload(payload: dict, secret: str) -> str:
    raw = json.dumps(payload, separators=(",", ":"), sort_keys=True).encode()
    return hmac.new(secret.encode(), raw, hashlib.sha256).hexdigest()

def build_webhook_payload(*, event_type, project_id, export_id, distribution_request_id, metadata=None):
    return {
        "event_type": event_type,
        "occurred_at": datetime.utcnow().isoformat(),
        "project_id": project_id,
        "export_id": export_id,
        "distribution_request_id": distribution_request_id,
        "metadata": metadata or {},
    }

def deliver_webhook(*, webhook, payload, secret):
    """
    Stub only.
    Real delivery + retries belong to Phase O.3.
    """
    signature = sign_payload(payload, secret)

    return {
        "delivered": False,
        "signature": signature,
        "payload": payload,
    }

