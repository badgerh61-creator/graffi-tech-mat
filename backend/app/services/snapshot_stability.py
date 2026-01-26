from datetime import datetime, timedelta

DRAFT_TTL = timedelta(hours=24)

def enforce_draft_ttl(snapshot):
    if snapshot.status != "draft":
        return

    if snapshot.created_at < datetime.utcnow() - DRAFT_TTL:
        snapshot.status = "abandoned"

