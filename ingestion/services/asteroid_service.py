import os
import requests

from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    Float,
    Boolean
)

from sqlalchemy.orm import (
    sessionmaker,
    declarative_base
)


DATABASE_URL = "postgresql://postgres:password@db:5432/space_db"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()


API_KEY = os.getenv(
    "NASA_API_KEY",
    "DEMO_KEY"
)


class Asteroid(Base):

    __tablename__ = "asteroids"

    id = Column(
        Integer,
        primary_key=True
    )

    name = Column(String)

    diameter = Column(Float)

    velocity = Column(Float)

    miss_distance = Column(Float)

    hazardous = Column(Boolean)

    close_approach_date = Column(String)


def fetch_asteroids():

    url = (
        f"https://api.nasa.gov/neo/rest/v1/feed"
        f"?api_key={API_KEY}"
    )

    response = requests.get(
        url,
        timeout=20
    )

    data = response.json()


    if (
        "near_earth_objects"
        not in data
    ):

        print(
            "Asteroids unavailable"
        )

        print(
            data
        )

        return


    db = SessionLocal()

    inserted = 0


    for date in data["near_earth_objects"]:

        for asteroid in data["near_earth_objects"][date]:


            if not asteroid["close_approach_data"]:

                continue


            clean_name = (

                asteroid["name"]

                .replace(
                    "(",
                    ""
                )

                .replace(
                    ")",
                    ""
                )

            )


            exists = (

                db.query(
                    Asteroid
                )

                .filter(
                    Asteroid.name
                    ==
                    clean_name
                )

                .first()

            )


            if exists:

                continue


            db.add(

                Asteroid(

                    name=
                    clean_name,

                    diameter=
                    asteroid[
                        "estimated_diameter"
                    ][
                        "meters"
                    ][
                        "estimated_diameter_max"
                    ],

                    velocity=
                    float(

                        asteroid[
                            "close_approach_data"
                        ][0][
                            "relative_velocity"
                        ][
                            "kilometers_per_hour"
                        ]

                    ),

                    miss_distance=
                    float(

                        asteroid[
                            "close_approach_data"
                        ][0][
                            "miss_distance"
                        ][
                            "kilometers"
                        ]

                    ),

                    hazardous=
                    asteroid[
                        "is_potentially_hazardous_asteroid"
                    ],

                    close_approach_date=
                    asteroid[
                        "close_approach_data"
                    ][0][
                        "close_approach_date"
                    ]

                )

            )

            inserted += 1


    db.commit()


    print(
        f"Added {inserted} asteroids"
    )