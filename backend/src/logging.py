import logging
from enum import StrEnum

LOG_FORMAT_DEBUG = "%(levelname)s:%(message)s:%(pathname)s:%(funcName)s:%(lineno)d"

class Loglevels(StrEnum):
    info = "INFO"
    warn = "WARN"
    error = "ERROR"
    debug = "DEBUG"

def configure_logging(log_level: str = Loglevels.error):
    log_level = str(log_level).upper()
    log_levels = [log_level.value for log_level in Loglevels]
    
    if log_level not in log_levels:
        logging.basicConfig(level=logging.error)
        return
    
    if log_level == Loglevels.debug:
        logging.basicConfig(level=log_level, format=LOG_FORMAT_DEBUG)
        return
    
    logging.basicConfig(level=log_level)
            