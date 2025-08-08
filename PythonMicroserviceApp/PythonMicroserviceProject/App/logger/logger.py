from loguru import logger
from App.config import LOG_FILE

def setup_logging():
    logger.add(LOG_FILE, rotation="1 MB", retention="7 days", level="INFO")
