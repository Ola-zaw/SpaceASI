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


DATABASE_URL = "postgresql://postgres:password@db:5432/space_db"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()


class APOD(Base):
    __tablename__ = "apod"

    id = Column(Integer, primary_key=True)

    title = Column(String)

    image_url = Column(Text)

    explanation = Column(Text)

    apod_date = Column(String)


def fetch_apod():

    url = (
        "https://api.nasa.gov/planetary/apod"
        "?api_key=DEMO_KEY"
    )

    response = requests.get(url)

    data = response.json()

    db = SessionLocal()

    new_apod = APOD(
        title=data["title"],
        image_url=data["url"],
        explanation=data["explanation"],
        apod_date=data["date"]
    )

    db.add(new_apod)

    db.commit()

    print("APOD saved!")