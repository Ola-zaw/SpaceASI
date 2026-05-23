import time

from services.iss_service import fetch_iss
from services.apod_service import fetch_apod
from services.asteroid_service import fetch_asteroids


print(
    "Starting ingestion..."
)


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


last_daily_update=time.time()


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
