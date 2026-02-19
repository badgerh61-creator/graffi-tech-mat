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

    def _prune(self, q: deque, now: float) -> None:
        # internal helper; does not change public API
        while q and (now - q[0]) > self.cfg.window_seconds:
            q.popleft()

    def allow(self, key: str) -> bool:
        """
        Backward-compatible:
        - Returns bool only (unchanged)
        """
        now = time.time()
        q = self.hits[key]

        self._prune(q, now)

        if len(q) >= self.cfg.max_requests:
            return False

        q.append(now)
        return True

    # ✅ Additive helpers (won't break existing imports/callers)
    def remaining(self, key: str) -> int:
        now = time.time()
        q = self.hits[key]
        self._prune(q, now)
        return max(0, self.cfg.max_requests - len(q))

    def reset_seconds(self, key: str) -> int:
        now = time.time()
        q = self.hits[key]
        self._prune(q, now)
        if not q:
            return 0
        oldest = q[0]
        reset_in = int(self.cfg.window_seconds - (now - oldest))
        return max(0, reset_in)


def login_rate_limiter() -> InMemoryRateLimiter:
    """
    Backward-compatible factory:
    - Keeps env var names exactly as you already use them.
    """
    max_req = int(os.getenv("LOGIN_RATE_LIMIT_MAX", "10"))
    window = int(os.getenv("LOGIN_RATE_LIMIT_WINDOW_SECONDS", "60"))
    return InMemoryRateLimiter(RateLimitConfig(window_seconds=window, max_requests=max_req))

