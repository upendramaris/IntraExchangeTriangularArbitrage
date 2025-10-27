import sys

from loguru import logger


def setup_logging():
    logger.remove()
    logger.add(
        sys.stdout,
        colorize=True,
        format="<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
        level="INFO",
    )
    logger.add(
        "logs/triarb_{time}.log",
        rotation="10 MB",
        retention="10 days",
        compression="zip",
        format="{time:YYYY-MM-DD HH:mm:ss.SSS} | {level: <8} | {name}:{function}:{line} - {message}",
        level="DEBUG",
        serialize=True, # for JSON logging
    )

    # Suppress verbose logs from libraries
    for lib in ["websockets", "asyncio", "sqlalchemy"]:
        logger.disable(lib)

