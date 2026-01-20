def is_under_legal_hold(record) -> bool:
    return getattr(record, "legal_hold", False)

