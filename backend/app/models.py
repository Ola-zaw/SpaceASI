from sqlalchemy import Column, Integer, Float, DateTime
from sqlalchemy.sql import func
from sqlalchemy import String, Text
from sqlalchemy import Boolean

from app.database import Base

class ISSPosition(Base):
    __tablename__ = "iss_positions"

    id = Column(Integer, primary_key=True, index=True)

    latitude = Column(Float)
    longitude = Column(Float)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

class APOD(Base):
    __tablename__ = "apod"

    id = Column(Integer, primary_key=True)

    title = Column(String)

    image_url = Column(Text)

    explanation = Column(Text)

    apod_date = Column(String)


class Asteroid(Base):
    __tablename__ = "asteroids"

    id = Column(Integer, primary_key=True)

    name = Column(
    String,
    unique=True)

    diameter = Column(Float)

    velocity = Column(Float)

    miss_distance = Column(Float)

    hazardous = Column(Boolean)

    close_approach_date = Column(String)
    