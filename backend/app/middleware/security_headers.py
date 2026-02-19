from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        resp: Response = await call_next(request)

        # Keep existing headers (do not remove/change keys)
        resp.headers["X-Content-Type-Options"] = "nosniff"
        resp.headers["X-Frame-Options"] = "DENY"
        resp.headers["Referrer-Policy"] = "no-referrer"
        resp.headers["Permissions-Policy"] = "geolocation=(), microphone=(), camera=()"

        # ✅ Additive hardening (safe defaults, won't break callers)
        # - prevent caching of authenticated/editor responses by default
        # If you already set Cache-Control elsewhere, we don't overwrite it.
        resp.headers.setdefault("Cache-Control", "no-store")

        # - reasonable defaults for legacy proxies/browsers
        resp.headers.setdefault("Pragma", "no-cache")

        return resp

