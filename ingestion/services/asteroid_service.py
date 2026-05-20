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


class Asteroid(Base):
    __tablename__ = "asteroids"

    id = Column(Integer, primary_key=True)

    name = Column(String)

    diameter = Column(Float)

    velocity = Column(Float)

    miss_distance = Column(Float)

    hazardous = Column(Boolean)

    close_approach_date = Column(String)


def fetch_asteroids():

    url = (
        "https://api.nasa.gov/neo/rest/v1/feed"
        "?api_key=DEMO_KEY"
    )

    response = requests.get(url)

    data = response.json()

    near_earth_objects = data["near_earth_objects"]

    db = SessionLocal()

    for date in near_earth_objects:

        asteroids = near_earth_objects[date]

        for asteroid in asteroids:

            new_asteroid = Asteroid(

                name=asteroid["name"],

                diameter=asteroid[
                    "estimated_diameter"
                ]["meters"][
                    "estimated_diameter_max"
                ],

                velocity=float(
                    asteroid[
                        "close_approach_data"
                    ][0][
                        "relative_velocity"
                    ][
                        "kilometers_per_hour"
                    ]
                ),

                miss_distance=float(
                    asteroid[
                        "close_approach_data"
                    ][0][
                        "miss_distance"
                    ][
                        "kilometers"
                    ]
                ),

                hazardous=asteroid[
                    "is_potentially_hazardous_asteroid"
                ],

                close_approach_date=asteroid[
                    "close_approach_data"
                ][0][
                    "close_approach_date"
                ]
            )

            db.add(new_asteroid)

    db.commit()

    print("Asteroids saved!")