import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

from rich.logging import RichHandler


def setup_logger(
    name: str = "app",
    log_file: str | Path = "logs/debug.log",
    console_level: int = logging.INFO,
    file_level: int = logging.DEBUG,
    max_bytes: int = 5
    * 1024
    * 1024,  # Also rotate mid-run if 5 MB is hit (0 = startup only)
    backup_count: int = 5,
    rotate_on_start: bool = True,
) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    logger.propagate = False

    if logger.handlers:
        return logger

    log_path = Path(log_file)
    log_path.parent.mkdir(parents=True, exist_ok=True)
    should_rotate_existing = (
        rotate_on_start
        and backup_count > 0
        and log_path.exists()
        and log_path.stat().st_size > 0
    )

    rich_handler = RichHandler(
        level=console_level,
        rich_tracebacks=True,
        show_time=True,
        show_path=False,
    )
    rich_handler.setFormatter(logging.Formatter("%(message)s"))

    file_handler = RotatingFileHandler(
        filename=log_path,
        mode="a",
        maxBytes=max_bytes,
        backupCount=backup_count,
        encoding="utf-8",
    )
    file_handler.setLevel(file_level)
    file_handler.setFormatter(
        logging.Formatter(
            "%(asctime)s | %(levelname)-8s | %(name)s:%(lineno)d | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
    )

    if should_rotate_existing:
        file_handler.doRollover()

    logger.addHandler(rich_handler)
    logger.addHandler(file_handler)
    return logger


log = setup_logger(
    name="EMC Config Generator",
    log_file="logs/debug.log",
    backup_count=5,
    rotate_on_start=True,
)

log.info("Starting Log!")
