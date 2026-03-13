import json
import logging
import sys
from datetime import datetime, timezone

from app.core.config import settings


class JsonFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        payload = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }
        if record.exc_info:
            payload["exception"] = self.formatException(record.exc_info)
        return json.dumps(payload, ensure_ascii=True)


def setup_logger() -> logging.Logger:
    logger = logging.getLogger(settings.APP_NAME)
    log_level = (settings.LOG_LEVEL or "").upper().strip() or ("DEBUG" if settings.DEBUG else "INFO")
    logger.setLevel(getattr(logging, log_level, logging.INFO))

    handler = logging.StreamHandler(sys.stdout)
    if settings.LOG_JSON:
        formatter = JsonFormatter()
    else:
        formatter = logging.Formatter("[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s")

    handler.setFormatter(formatter)

    if not logger.handlers:
        logger.addHandler(handler)

    logger.propagate = False
    return logger


logger = setup_logger()
