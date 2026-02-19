import os
import time
from collections import defaultdict, deque
from dataclasses import dataclass


@dataclass(frozen=True)
class RateLimitConfig:
    window_seconds: int
    max_requests: int


class InMemoryRateLimiter:
    def __init__(self, cfg: RateLimitConfig):
        self.cfg = cfg
        self.hits = defaultdict(deque)

    def allow(self, key: str) -> bool:
        now = time.time()
        q = self.hits[key]

        while q and (now - q[0]) > self.cfg.window_seconds:
            q.popleft()

        if len(q) >= self.cfg.max_requests:
            return False

        q.append(now)
        return True


def login_rate_limiter() -> InMemoryRateLimiter:
    max_req = int(os.getenv("LOGIN_RATE_LIMIT_MAX", "10"))
    window = int(os.getenv("LOGIN_RATE_LIMIT_WINDOW_SECONDS", "60"))
    return InMemoryRateLimiter(RateLimitConfig(window_seconds=window, max_requests=max_req))

