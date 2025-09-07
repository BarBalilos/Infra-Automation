import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

def setup_logger(log_file: Path) -> logging.Logger:
    logger = logging.getLogger("infra_simulator")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    if not logger.handlers:
        formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")

        file_handler = RotatingFileHandler(
            log_file, maxBytes=250 * 1024, backupCount=2, encoding="utf-8"
        )
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

    return logger
