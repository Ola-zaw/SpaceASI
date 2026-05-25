from contextlib import contextmanager
import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import (
    engine,
    SessionLocal
)

from app.models import (
    Base,
    ISSPosition,
    Asteroid,
    APOD
)

from datetime import (
    date,
    timedelta
)




print(
    Base.metadata.tables.keys()
)


app = FastAPI()


app.add_middleware(

    CORSMiddleware,

    allow_origins=["*"],

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"]

)


Base.metadata.create_all(
    bind=engine
)



@contextmanager
def get_db():

    db = SessionLocal()

    try:

        yield db

    finally:

        db.close()



@app.get(

"/",

summary=
"API status"

)
def root():

    return {

        "service":
        "Space Dashboard API",

        "status":
        "running",

        "environment":

        os.getenv(
            "APP_ENV"
        ),

        "docs":

        "/docs"

    }



@app.get(

    "/iss/latest",

    summary=
    "Get current ISS position",

    description=
    """
    Returns latest recorded position of the
    International Space Station.
    Updated every 5 seconds.
    """

)
def get_latest_iss():

    with get_db() as db:

        latest = (

            db.query(
                ISSPosition
            )

            .order_by(
                ISSPosition.id.desc()
            )

            .first()

        )


        if latest is None:

            return {

                "id": 0,

                "latitude": 0,

                "longitude": 0,

                "created_at": None

            }


        return {

            "id":
            latest.id,

            "latitude":
            latest.latitude,

            "longitude":
            latest.longitude,

            "created_at":
            latest.created_at

        }



@app.get(

"/iss/history",

summary=
"Get ISS trajectory",

description=
"Returns historical ISS positions used to draw the trail (last 500 points)."

)
def get_iss_history():

    with get_db() as db:

        history = (

            db.query(
                ISSPosition
            )

            .order_by(
                ISSPosition.created_at.desc()
            )

            .limit(
                500
            )

            .all()

        )


        history.reverse()


        return [

            {

                "latitude":
                x.latitude,

                "longitude":
                x.longitude,

                "created_at":
                x.created_at

            }

            for x
            in history

        ]


@app.get(

"/asteroids",

summary=
"Get asteroid approaches",

description=
"""
Returns asteroid approaches
for the next 7 days.
"""

)
def get_asteroids():

    with get_db() as db:


        today = str(
            date.today()
        )


        week = str(

            date.today()

            +

            timedelta(
                days=7
            )

        )


        rows = (

            db.query(
                Asteroid
            )

            .filter(

                Asteroid.close_approach_date

                >=

                today

            )

            .filter(

                Asteroid.close_approach_date

                <=

                week

            )

            .order_by(

                Asteroid.close_approach_date.asc()

            )

            .all()

        )


        return [

            {

                "key":

                f"{x.name}_{x.close_approach_date}",

                "name":
                x.name,

                "diameter":
                round(
                    x.diameter
                ),

                "velocity":
                round(
                    x.velocity
                ),

                "miss_distance":
                round(
                    x.miss_distance
                ),

                "hazardous":
                x.hazardous,

                "date":
                x.close_approach_date

            }

            for x

            in rows

        ]



@app.get(

"/asteroids/stats",

summary=
"Get asteroid statistics",

description=
"""
Returns:
- total approaches
- hazardous approaches
- date range
"""

)
def asteroid_stats():

    with get_db() as db:

        today = date.today()

        week = (

            today

            +

            timedelta(
                days=7
            )

        )


        rows = (

            db.query(
                Asteroid
            )

            .all()

        )


        values = [

            x

            for x

            in rows

            if

            today

            <=

            date.fromisoformat(
                x.close_approach_date
            )

            <=

            week

        ]


        unique = {

            (

                x.name,

                x.close_approach_date

            )

            :

            x

            for x

            in rows

        }


        values = list(
            unique.values()
        )


        if not values:

            return {

                "total":0,

                "hazardous":0,

                "start_date":"",

                "end_date":""

            }


        return {

            "total":

            len(
                values
            ),

            "hazardous":

            len(

                [

                    x

                    for x

                    in values

                    if x.hazardous

                ]

            ),

            "start_date":

            min(

                x.close_approach_date

                for x

                in values

            ),

            "end_date":

            max(

                x.close_approach_date

                for x

                in values

            )

        }


@app.get(

"/apod/latest",

summary=
"Get Astronomy Picture of the Day",

description=
"""
Returns latest APOD image
or video with description.
"""

)
def get_latest_apod():

    with get_db() as db:

        latest = (

            db.query(
                APOD
            )

            .order_by(
                APOD.id.desc()
            )

            .first()

        )


        if latest is None:

            return {

                "title":
                "No APOD",

                "image_url":
                "",

                "explanation":
                "NASA unavailable",

                "date":
                ""

            }


        return {

            "title":
            latest.title,

            "image_url":
            latest.image_url,

            "explanation":
            latest.explanation,

            "date":
            latest.apod_date

        }
    