from __future__ import annotations

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse

from app.core.security_settings import SecuritySettings
from app.services.rate_limiter import InMemoryRateLimiter, RateLimitConfig


class LoginRateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, settings: SecuritySettings):
        super().__init__(app)
        self.settings = settings
        self.limiter = InMemoryRateLimiter(
            RateLimitConfig(
                window_seconds=settings.login_rate_limit_window_seconds,
                max_requests=settings.login_rate_limit_max_requests,
            )
        )

    async def dispatch(self, request: Request, call_next):
        # Only guard POST /login
        if request.method.upper() == "POST" and request.url.path == "/login":
            ip = request.client.host if request.client else "unknown"

            if not self.limiter.allow(f"login:{ip}"):
                return JSONResponse(
                    status_code=429,
                    content={"detail": "Rate limit exceeded"},
                )

        return await call_next(request)

