import logging
from typing import Optional


# PUBLIC_INTERFACE
def configure_logging(level: int = logging.INFO, fmt: Optional[str] = None) -> None:
    """Configure application-wide logging with a structured, safe format.

    Args:
        level: Logging level, defaults to logging.INFO.
        fmt: Optional custom log format.
    """
    log_format = fmt or (
        "%(asctime)s %(levelname)s [%(name)s] %(message)s"
    )
    # Use basicConfig only once; further calls are no-ops
    logging.basicConfig(level=level, format=log_format)
