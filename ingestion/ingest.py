import time

from services.iss_service import fetch_iss
from services.apod_service import fetch_apod
from services.asteroid_service import fetch_asteroids
import logging

logging.basicConfig(

    level=logging.INFO,

    format="%(asctime)s | %(levelname)s | %(message)s"

)

logger = logging.getLogger(__name__)


logger.info(
    "Starting ingestion..."
)


try:

    fetch_apod()

    logger.info(
        "APOD updated"
    )

except Exception as e:

    logger.error(
        f"APOD ERROR: {e}"
    )


try:

    fetch_asteroids()

    logger.info(
        "Asteroids updated"
    )

except Exception as e:

    logger.error(
        f"Asteroids ERROR: {e}"
    )

last_daily_update=time.time()


while True:

    try:

        fetch_iss()

        logger.info(
            "ISS updated"
        )

    except Exception as e:

        logger.error(
            f"ISS ERROR: {e}"
        )


    now = time.time()


    if (

        now

        -

        last_daily_update

        >

        86400

    ):

        try:

            fetch_apod()

            print(
                "APOD updated"
            )

        except Exception as e:

            print(
                "APOD ERROR:",
                e
            )


        try:

            fetch_asteroids()

            print(
                "Asteroids updated"
            )

        except Exception as e:

            print(
                "ASTEROIDS ERROR:",
                e
            )


        last_daily_update = now


    time.sleep(5)
