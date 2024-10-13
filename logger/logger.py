import logging
import logging.handlers
import os
from pathlib import Path


def setup_logger(
    name: str, log_file: str = "app.log", level: int = logging.INFO
) -> logging.Logger:
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)

    logger = logging.getLogger(name)
    logger.setLevel(level)

    if not logger.hasHandlers():
        console_handler = logging.StreamHandler()
        console_handler.setLevel(level)

        file_handler = logging.handlers.RotatingFileHandler(
            log_dir / log_file, maxBytes=5 * 1024 * 1024, backupCount=5
        )
        file_handler.setLevel(level)

        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        console_handler.setFormatter(formatter)
        file_handler.setFormatter(formatter)

        logger.addHandler(console_handler)
        logger.addHandler(file_handler)

    return logger


if __name__ == "__main__":
    logger = setup_logger(__name__)
