# Phase Q — Compliance & Retention

## Purpose
Define retention, purge, and compliance guarantees for all authoritative records.

---

## Record Classes

### Immutable (Never Deleted)
- Audit records (Phase N.4)
- Export artifacts (Phase M)
- Automation job logs (Phase O)
- Compliance reports

### Retained (Policy-Governed)
- Snapshots
- Workspaces
- Assets
- Metrics aggregates

---

## Retention Policy Schema

```json
{
  "record_type": "snapshot | export | audit | job_log | metric",
  "min_days": 30,
  "max_days": 365,
  "legal_hold": false
}

