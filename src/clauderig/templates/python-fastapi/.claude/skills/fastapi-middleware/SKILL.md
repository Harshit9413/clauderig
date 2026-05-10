---
name: fastapi-middleware
description: FastAPI middleware patterns — request logging, rate limiting, CORS, and custom error handling.
---

# FastAPI Middleware Patterns

## Request Logging Middleware

```python
# app/middleware/logging.py
import time
import uuid
import logging
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

logger = logging.getLogger(__name__)


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next) -> Response:
        request_id = str(uuid.uuid4())[:8]
        start = time.perf_counter()

        logger.info("%s %s %s started", request_id, request.method, request.url.path)

        try:
            response = await call_next(request)
        except Exception as exc:
            logger.exception("%s unhandled error", request_id)
            raise

        elapsed = (time.perf_counter() - start) * 1000
        logger.info(
            "%s %s %s → %d  %.1fms",
            request_id,
            request.method,
            request.url.path,
            response.status_code,
            elapsed,
        )
        response.headers["X-Request-ID"] = request_id
        return response
```

## Rate Limiting Middleware (slowapi)

```python
# pip install slowapi
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from fastapi import FastAPI

limiter = Limiter(key_func=get_remote_address, default_limits=["100/minute"])

app = FastAPI()
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Per-route limit
@router.post("/auth/token")
@limiter.limit("5/minute")
async def login(request: Request, form: OAuth2PasswordRequestForm = Depends()):
    ...
```

## CORS

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://myapp.com"],   # production
    # allow_origins=["*"],                 # dev only
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["Authorization", "Content-Type"],
)
```

## Global Exception Handler

```python
# app/middleware/errors.py
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError


def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(IntegrityError)
    async def db_integrity_error(request: Request, exc: IntegrityError):
        return JSONResponse(
            status_code=409,
            content={"detail": "Resource already exists or constraint violated."},
        )

    @app.exception_handler(ValueError)
    async def value_error(request: Request, exc: ValueError):
        return JSONResponse(status_code=400, content={"detail": str(exc)})

    @app.exception_handler(Exception)
    async def unhandled_error(request: Request, exc: Exception):
        logger.exception("Unhandled error on %s %s", request.method, request.url)
        return JSONResponse(status_code=500, content={"detail": "Internal server error."})
```

## Attaching Middleware

```python
# app/main.py
from app.middleware.logging import RequestLoggingMiddleware
from app.middleware.errors import register_exception_handlers

app = FastAPI()

app.add_middleware(RequestLoggingMiddleware)
register_exception_handlers(app)
```

## Trusted Hosts

```python
from starlette.middleware.trustedhost import TrustedHostMiddleware

app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["myapp.com", "*.myapp.com", "localhost"],
)
```
