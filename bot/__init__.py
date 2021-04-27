import os
import sys

from loguru import logger

sys.path.append(os.path.dirname(os.path.realpath(__file__)))


___VERSION___ = "[v1.0.0]"

config = {
    "handlers": [
        {"sink": sys.stdout,
         "format": ___VERSION___ + " [{time:YYYY-MM-DD at HH:mm:ss}] [{level}]: {message}"}
    ],
}

logger.configure(**config)

logger.info("Now loading...")
