IMMUTABLE_RECORD_TYPES = {
    "audit",
    "export",
    "automation_log",
    "compliance_report",
}

DEFAULT_RETENTION = {
    "snapshot": {"min_days": 30, "max_days": 365},
    "workspace": {"min_days": 30, "max_days": 365},
    "asset": {"min_days": 30, "max_days": 365},
    "metric": {"min_days": 7, "max_days": 90},
}

