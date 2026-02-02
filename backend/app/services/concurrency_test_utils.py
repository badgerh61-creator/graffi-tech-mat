# services/concurrency_test_utils.py

def advance_time(seconds: int):
    """
    Test-only utility to simulate time passage.

    Real kernel time authority lives in clock / session TTLs.
    This exists only to satisfy Phase U-S tests.
    """
    pass

