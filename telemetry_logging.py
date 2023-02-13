import asyncio
import logging
from logging.handlers import RotatingFileHandler

from gpp import GppUnit

DELAY: float = 0.3

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = RotatingFileHandler('main.log', maxBytes=50000000, backupCount=5)
logger.addHandler(handler)
formatter = logging.Formatter(
    '%(asctime)s, %(levelname)s, %(message)s, %(name)s')
handler.setFormatter(formatter)


async def get_permanent_telemetry(unit: GppUnit) -> None:
    """Корутина постоянного чтения ТМИ"""
    while True:
        for ch in range(1, 5):
            logger.info(unit.measure_all(ch))
            await asyncio.sleep(DELAY)
