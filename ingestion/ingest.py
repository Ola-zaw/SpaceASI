import time

from services.iss_service import fetch_iss
from services.apod_service import fetch_apod
from services.asteroid_service import fetch_asteroids


print(
    "Starting ingestion..."
)


try:

    fetch_apod()

except Exception as e:

    print(
        "APOD ERROR:",
        e
    )


try:

    fetch_asteroids()

except Exception as e:

    print(
        "ASTEROIDS ERROR:",
        e
    )


while True:

    try:

        fetch_iss()

        print(
            "ISS updated"
        )

    except Exception as e:

        print(
            "ISS ERROR:",
            e
        )

    time.sleep(5)
    