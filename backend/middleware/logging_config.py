"""Centralized logging configuration module for the Nexo API."""

import logging
from pathlib import Path


def setup_logging() -> None:
    """Configures system-wide logging redirection exclusively to a log file."""
    backend_dir: Path = Path(__file__).resolve().parent.parent
    log_dir: Path = backend_dir / "logs"
    log_dir.mkdir(exist_ok=True)

    log_file_path: Path = log_dir / "app.log"

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        filename=str(log_file_path),
        filemode="a",
        force=True,
    )

    for logger_name in ("uvicorn", "uvicorn.access", "uvicorn.error", "fastapi"):
        logger: logging.Logger = logging.getLogger(logger_name)
        logger.handlers = []
        logger.propagate = True