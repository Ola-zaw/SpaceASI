import time
import logging

from services.iss_service import fetch_iss
from services.apod_service import fetch_apod
from services.asteroid_service import fetch_asteroids

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

logger = logging.getLogger(__name__)

logger.info("Starting ingestion...")

# Pierwsze pobranie danych zaraz po starcie
try:
    fetch_apod()
    logger.info("APOD updated")
except Exception as e:
    logger.error(f"APOD ERROR: {e}")

try:
    fetch_asteroids()
    logger.info("Asteroids updated")
except Exception as e:
    logger.error(f"Asteroids ERROR: {e}")

last_daily_update = time.time()

while True:
    
    # ISS aktualizowany co 5 sekund
    try:
        fetch_iss()
        logger.info("ISS updated")
    except Exception as e:
        logger.error(f"ISS ERROR: {e}")

    now = time.time()

    # APOD i Asteroidy aktualizowane raz na dobę (86400 sekund)
    if now - last_daily_update > 86400:
        try:
            fetch_apod()
            logger.info("APOD updated")
        except Exception as e:
            logger.error(f"APOD ERROR: {e}")

        try:
            fetch_asteroids()
            logger.info("Asteroids updated")
        except Exception as e:
            logger.error(f"ASTEROIDS ERROR: {e}")

        last_daily_update = now

    time.sleep(5)
