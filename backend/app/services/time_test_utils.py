"""
Test-only time manipulation utilities.
Never imported into production code.
"""

from datetime import timedelta
from app.services.clock import clock  # your authoritative time source

def advance_time(seconds: int):
    clock.advance(timedelta(seconds=seconds))

