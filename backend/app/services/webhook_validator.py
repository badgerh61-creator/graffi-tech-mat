from urllib.parse import urlparse

from app.services.automation_capabilities import compute_automation_capabilities
from app.services.webhook_policies import SUPPORTED_WEBHOOK_EVENTS

def validate_webhook_configuration(*, user, project, url, events):
    # Project gate
    if getattr(project, "archived", False) or getattr(project, "suspended", False):
        return {"allowed": False, "reason": "project_disabled"}

    # Capability gate (Phase O.0)
    caps = compute_automation_capabilities(
        user=user,
        project=project,
    )

    if not caps["canConfigureIntegrations"]:
        return {"allowed": False, "reason": "capability_missing"}

    # HTTPS enforcement
    parsed = urlparse(url)
    if parsed.scheme != "https":
        return {"allowed": False, "reason": "https_required"}

    # Event allowlist
    if not events or not set(events).issubset(SUPPORTED_WEBHOOK_EVENTS):
        return {"allowed": False, "reason": "invalid_events"}

    return {
        "allowed": True,
        "url": url,
        "events": events,
    }

