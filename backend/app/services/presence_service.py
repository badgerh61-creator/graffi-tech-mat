# Phase U.1 — Presence authority (minimal, compliant)

_present_users: set[int] = set()

def mark_user_present(user):
    _present_users.add(user.id)

def mark_user_absent(user):
    _present_users.discard(user.id)

def is_user_present(user):
    return user.id in _present_users

