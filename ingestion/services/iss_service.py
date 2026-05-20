import requests

from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    Float,
    DateTime
)

from sqlalchemy.orm import (
    sessionmaker,
    declarative_base
)

from sqlalchemy.sql import func


DATABASE_URL = "postgresql://postgres:password@db:5432/space_db"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()


class ISSPosition(Base):
    __tablename__ = "iss_positions"

    id = Column(Integer, primary_key=True)

    latitude = Column(Float)
    longitude = Column(Float)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )


def fetch_iss():

    response = requests.get(
        "http://api.open-notify.org/iss-now.json"
    )

    data = response.json()

    latitude = float(
        data["iss_position"]["latitude"]
    )

    longitude = float(
        data["iss_position"]["longitude"]
    )

    db = SessionLocal()

    new_position = ISSPosition(
        latitude=latitude,
        longitude=longitude
    )

    db.add(new_position)

    db.commit()

    print("ISS position saved!")