"""
logging_config.py — Centralised logging setup.

File handler  : DEBUG and above → logs/bot.log (rotating, 5 MB × 3 backups)
Console handler: WARNING and above → terminal (keeps output clean)
"""

import logging
import logging.handlers
import os

LOG_DIR = "logs"
LOG_FILE = os.path.join(LOG_DIR, "bot.log")

_CONFIGURED = False


def setup_logging(console_level: str = "WARNING") -> None:
    """
    Configure root logger. Safe to call multiple times — only initialises once.

    Args:
        console_level: Minimum log level shown in terminal (default: WARNING).
                       File always captures DEBUG and above.
    """
    global _CONFIGURED
    if _CONFIGURED:
        return

    os.makedirs(LOG_DIR, exist_ok=True)

    root = logging.getLogger()
    root.setLevel(logging.DEBUG)  # let handlers decide what to display

    # ── File handler — rotating, captures everything ───────────────────────────
    file_handler = logging.handlers.RotatingFileHandler(
        LOG_FILE,
        maxBytes=5 * 1024 * 1024,   # 5 MB per file
        backupCount=3,               # keep bot.log, bot.log.1, bot.log.2, bot.log.3
        encoding="utf-8",
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(logging.Formatter(
        fmt="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    ))

    # ── Console handler — clean terminal output ───────────────────────────────
    console_handler = logging.StreamHandler()
    console_handler.setLevel(getattr(logging, console_level.upper(), logging.WARNING))
    console_handler.setFormatter(logging.Formatter(
        fmt="%(levelname)-8s %(message)s"
    ))

    root.addHandler(file_handler)
    root.addHandler(console_handler)

    _CONFIGURED = True

    logging.getLogger(__name__).info(
        "Logging initialised — file=%s console_level=%s", LOG_FILE, console_level
    )
