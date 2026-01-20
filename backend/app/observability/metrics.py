from collections import defaultdict
import time

class MetricsCollector:
    def __init__(self):
        self._counters = defaultdict(int)
        self._timings = defaultdict(list)

    def inc(self, name, value=1):
        self._counters[name] += value

    def timing(self, name, duration_ms):
        self._timings[name].append(duration_ms)

    def count(self, name):
        return self._counters.get(name, 0)

metrics = MetricsCollector()

