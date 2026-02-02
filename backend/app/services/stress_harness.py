# services/stress_harness.py

import threading

def run_concurrent(tasks):
    """
    Executes callables concurrently for stress testing.
    Test-only utility. No kernel logic.
    """
    threads = [threading.Thread(target=t) for t in tasks]

    for t in threads:
        t.start()

    for t in threads:
        t.join()

