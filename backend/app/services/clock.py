from datetime import datetime, timedelta

class KernelClock:
    def __init__(self):
        self._offset = timedelta(0)

    def now(self) -> datetime:
        return datetime.utcnow() + self._offset

    def advance(self, delta: timedelta):
        self._offset += delta


# 🔒 SINGLE AUTHORITATIVE CLOCK
clock = KernelClock()

