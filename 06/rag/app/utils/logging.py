import logging
import os
from logging.handlers import RotatingFileHandler

LOG_FILE_PATH = "logs/app.log"
os.makedirs(os.path.dirname(LOG_FILE_PATH), exist_ok=True)

file_formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
file_handler = RotatingFileHandler(
    LOG_FILE_PATH, maxBytes=5 * 1024 * 1024, backupCount=3, encoding="utf-8"
)
file_handler.setFormatter(file_formatter)
file_handler.setLevel(logging.INFO)

uvicorn_loggers = ["uvicorn", "uvicorn.error", "uvicorn.access"]
for logger_name in uvicorn_loggers:
    logging.getLogger(logger_name).addHandler(file_handler)

logging.getLogger("uvicorn.access").propagate = False

logger = logging.getLogger("uvicorn.error")
