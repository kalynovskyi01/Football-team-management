import os
import logging
import structlog

# --- LOGGING CONFIGURATION ---
def logconf():
IS_PRODUCTION = os.getenv("ENVIRONMENT") == "Production"

    shared_processors = [
        structlog.contextvars.merge_contextvars,
        structlog.processors.add_log_level,
        structlog.processors.StackInfoRenderer(),
        structlog.dev.set_exc_info,
        structlog.processors.TimeStamper(fmt="iso", utc=True),
        structlog.processors.format_exc_info,
    ]

    processors = shared_processors + (
        [structlog.processors.JSONRenderer()]
        if IS_PRODUCTION
        else [structlog.dev.ConsoleRenderer()]
    )

    structlog.configure(
        processors=processors,
        wrapper_class=structlog.make_filtering_bound_logger(logging.INFO),
        context_class=dict,
        logger_factory=structlog.PrintLoggerFactory(),
        cache_logger_on_first_use=True,
    )

    logging.basicConfig(format="%(message)s", level=logging.INFO)

    logger = structlog.get_logger()

def get_client_ip(request: Request) -> str:
    """Get the real client IP, accounting for the nginx reverse proxy.
 
    nginx sets X-Forwarded-For; without it, request.client.host would just
    be nginx's own internal IP, not the actual visitor.
    """
    forwarded_for = request.headers.get("x-forwarded-for")
    if forwarded_for:
        # X-Forwarded-For can be a comma-separated chain of proxies;
        # the first entry is the original client.
        return forwarded_for.split(",")[0].strip()
    return request.client.host if request.client else "unknown"