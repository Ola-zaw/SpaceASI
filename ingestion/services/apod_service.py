import os
import requests

from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    Text
)

from sqlalchemy.orm import (
    sessionmaker,
    declarative_base
)

DATABASE_URL =os.getenv(
"DATABASE_URL"
)

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()


API_KEY = os.getenv(
    "NASA_API_KEY",
    "DEMO_KEY"
)


class APOD(Base):

    __tablename__ = "apod"

    id = Column(
        Integer,
        primary_key=True
    )

    title = Column(String)

    image_url = Column(Text)

    explanation = Column(Text)

    apod_date = Column(String)


def fetch_apod():

    url = (
        f"https://api.nasa.gov/planetary/apod"
        f"?api_key={API_KEY}"
    )

    response = requests.get(
        url,
        timeout=20
    )

    data = response.json()


    if "title" not in data:

        print(
            "APOD unavailable"
        )

        print(
            data
        )

        return


    db = SessionLocal()


    new_apod = APOD(

        title=data["title"],

        image_url=data["url"],

        explanation=data["explanation"],

        apod_date=data["date"]

    )


    db.add(
        new_apod
    )

    db.commit()

    count = (

    db.query(
        APOD
    )

    .count()

    )


    if count > 30:

        remove = (

            db.query(
                APOD
            )

            .order_by(
                APOD.id.asc()
            )

            .limit(
                count - 30
            )

            .all()

        )


        for row in remove:

            db.delete(
                row
            )


        db.commit()


    print(
        "APOD saved!"
    )
    