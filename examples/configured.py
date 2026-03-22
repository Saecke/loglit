"""Fully configured example - all options customized."""
import logging
from loglit import configure, log, printlog

configure(
    log_dir="my_logs",
    encoding="utf-8",
    log_level=logging.DEBUG,
    log_format="%(asctime)s [%(levelname)s] %(message)s",
    date_format="%Y-%m-%d %H:%M:%S",
    file_prefix="myapp_",
    file_suffix="_debug",
    file_extension="txt",
    file_timestamp="%Y%m%d_%H%M%S",
)

log("Only in file.", level=logging.DEBUG)
printlog("App started.", level=logging.INFO)
printlog("Disk almost full.", level=logging.WARNING)
printlog("Connection failed.", level=logging.ERROR)
