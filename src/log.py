from loguru import logger
import sys
from pathlib import Path

log_path = Path(__file__).parent.parent / "logs" / "{time:YYYY-MM-DD}.log"

logger.add(
    sink=log_path,
    rotation="daily",
    colorize=True,
    format="{time:YY-MM-DD HH:mm:ss} | {level} | {message}",
)


def write_log(message):
    logger.info(message)
    sys.stdout.flush()
    sys.stderr.flush()
