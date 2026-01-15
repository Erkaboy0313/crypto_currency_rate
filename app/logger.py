# apps/prices/logger.py
import logging
from logging.handlers import RotatingFileHandler
import os

# Ensure logs folder exists
os.makedirs("logs", exist_ok=True)

# Create a logger
logger = logging.getLogger("price_logger")
logger.setLevel(logging.INFO)  # Minimum level to log

# Formatter
formatter = logging.Formatter(
    "%(asctime)s [%(levelname)s] [%(name)s] %(message)s"
)

# Stream handler (stdout)
stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.INFO)
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)

# File handler (rotates 5MB, keeps 3 backups)
file_handler = RotatingFileHandler("logs/app.log", maxBytes=5*1024*1024, backupCount=3)
file_handler.setLevel(logging.WARNING)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
