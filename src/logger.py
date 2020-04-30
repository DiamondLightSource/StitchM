import sys
from pathlib import Path
import logging
from logging.handlers import TimedRotatingFileHandler

level_dict = {
    "1": logging.DEBUG,
    "2": logging.INFO,
    "3": logging.WARNING,
    "4": logging.ERROR,
    "5": logging.CRITICAL,
    "debug": logging.DEBUG,
    "info": logging.INFO,
    "warn": logging.WARNING,
    "warning": logging.WARNING,
    "error": logging.ERROR,
    "critical": logging.CRITICAL,
    }

logpath = Path("logs")
LOG_FILE = logpath / "stitch_m_log"


def create_logger(file_level="debug", stream_level="error", backup_count=10):
    """
    Creates a logging file handler that creates a new file daily at midnight, with up to 'backup_count' log files saved.
    This also sets logging for stdout to info level.
    
    INPUTS:
    file_level (string or int), stream_level (string or int), backup_count (int)
    
    ACCEPTABLE LOGGING LEVELS:
    debug OR 1
    info OR 2
    warn OR warning OR 3
    error OR 4
    Critical OR 5
    
    Alternatively will default to debug.
    """
    if not logpath.is_dir():
        logpath.mkdir(mode=0o777)
    if file_level in level_dict:
        file_level = level_dict[file_level]
    else:
        # use debug if no valid logging level is passed
        file_level = logging.DEBUG
        logging.error(f"Invalid logging level passed - see docstring")
    if stream_level in level_dict:
        stream_level = level_dict[stream_level]
    else:
        # use debug if no valid logging level is passed
        stream_level = logging.ERROR
        logging.error(f"Invalid logging level passed - see docstring")

    stream_handler = logging.StreamHandler(sys.stdout)
    stream_format = logging.Formatter("%(levelname)-8s %(filename)s|%(funcName)s: %(message)s")
    stream_handler.setFormatter(stream_format)

    file_handler = TimedRotatingFileHandler(str(LOG_FILE), when='midnight', interval=1, backupCount=backup_count)
    file_format = logging.Formatter("%(asctime)s %(levelname)-8s %(filename)s|%(funcName)s: %(message)s", datefmt="%d %b %Y - %H:%M:%S")
    file_handler.setFormatter(file_format)

    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    stream_handler.setLevel(stream_level)
    logger.addHandler(stream_handler)
    file_handler.setLevel(file_level)
    logger.addHandler(file_handler)
