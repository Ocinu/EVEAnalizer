import logging
import os

from loguru import logger


class InterceptHandler(logging.Handler):
    def emit(self, record):
        logger_opt = logger.opt(depth=6, exception=record.exc_info)
        logger_opt.log(record.levelno, record.getMessage())


logging.basicConfig(handlers=[InterceptHandler()], level=0)

logger.configure(
    handlers=[
        {"sink": os.path.join("logs", "logs.log"), "level": "INFO", "rotation": "1 day"}
    ]
)
