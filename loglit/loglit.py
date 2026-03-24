"""
loglit - Lightweight logging for Python. One import, no boilerplate.

Features:
- log() for file logging, printlog() for console + file logging
- configure() to customize without editing source code
- Automatic timestamped log files
- UTF-8 log files by default

Author: FMJ
License: MIT
"""
import os
import sys
import logging
from datetime import datetime

# --- Internal State ---
_config = {
    "log_dir": os.path.join("loglit", "logs"),
    "logger_name": "loglit",
    "log_level": logging.DEBUG,
    "log_format": "%(asctime)s - %(message)s",
    "date_format": "%d-%m-%Y %H:%M:%S",
    "encoding": "utf-8",
    "file_prefix": "loglit_",
    "file_suffix": "",
    "file_extension": "log",
    "file_timestamp": "%d-%m-%Y_%H-%M-%S",
}

_file_logger = None
_print_logger = None
_initialized = False


def _generate_log_filename():
    timestamp = datetime.now().strftime(_config["file_timestamp"])
    name = f"{_config['file_prefix']}{timestamp}{_config['file_suffix']}"
    return os.path.join(_config["log_dir"], f"{name}.{_config['file_extension']}")


def _setup_logger():
    global _file_logger, _print_logger, _initialized

    os.makedirs(_config["log_dir"], exist_ok=True)

    formatter = logging.Formatter(
        _config["log_format"], datefmt=_config["date_format"]
    )

    file_handler = logging.FileHandler(
        _generate_log_filename(), encoding=_config["encoding"]
    )
    file_handler.setLevel(_config["log_level"])
    file_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler(stream=sys.stderr)
    console_handler.setLevel(_config["log_level"])
    console_handler.setFormatter(formatter)

    # Close old handlers before replacing (prevents file handle leaks)
    if _file_logger or _print_logger:
        closed = set()
        for logger in (_file_logger, _print_logger):
            if logger:
                for h in logger.handlers:
                    if h not in closed:
                        h.close()
                        closed.add(h)
                logger.handlers.clear()

    # log() → file only
    _file_logger = logging.getLogger(_config["logger_name"] + ".file")
    _file_logger.setLevel(_config["log_level"])
    _file_logger.addHandler(file_handler)
    _file_logger.propagate = False

    # printlog() → file + console
    _print_logger = logging.getLogger(_config["logger_name"] + ".print")
    _print_logger.setLevel(_config["log_level"])
    _print_logger.addHandler(file_handler)
    _print_logger.addHandler(console_handler)
    _print_logger.propagate = False

    _initialized = True


def _ensure_initialized():
    if not _initialized:
        _setup_logger()


# --- Public API ---
def configure(**kwargs):
    """Configure the logger. Call before the first log() or printlog().

    Keyword arguments:
        log_dir (str):          Directory for log files. Default: loglit/logs/
        encoding (str):         Log file encoding. Default: utf-8
        log_level (int):        Minimum log level. Default: logging.DEBUG
        log_format (str):       Log line format. Default: %(asctime)s - %(message)s
        date_format (str):      Timestamp format. Default: %d-%m-%Y %H:%M:%S
        file_prefix (str):      Filename prefix. Default: loglit_
        file_suffix (str):      Filename suffix (after timestamp). Default: ""
        file_extension (str):   File extension. Default: log
        file_timestamp (str):   Timestamp format in filename. Default: %d-%m-%Y_%H-%M-%S
    """
    for key, value in kwargs.items():
        if key not in _config:
            raise ValueError(f"Unknown config option: '{key}'")
        _config[key] = value

    # (Re)initialize logger with new config
    _setup_logger()


def log(message, level=logging.INFO):
    """Log a message to file only."""
    _ensure_initialized()
    _file_logger.log(level, message)


def printlog(message, level=logging.INFO):
    """Log a message to console and file."""
    _ensure_initialized()
    _print_logger.log(level, message)
