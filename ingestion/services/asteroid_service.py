import os
from datetime import date, timedelta
import requests

from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

API_KEY = os.getenv("NASA_API_KEY", "DEMO_KEY")


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
    url = f"https://api.nasa.gov/neo/rest/v1/feed"
    
    today = date.today()
    week_end = today + timedelta(days=7)

    response = requests.get(
        url,
        params={
            "start_date": today,
            "end_date": week_end,
            "api_key": API_KEY
        },
        timeout=20
    )
    
    data = response.json()

    if "near_earth_objects" not in data:
        print("Asteroids unavailable")
        print(data)
        return

    db = SessionLocal()
    inserted = 0

    for day in data["near_earth_objects"]:
        for asteroid in data["near_earth_objects"][day]:
            
            if not asteroid["close_approach_data"]:
                continue

            clean_name = asteroid["name"].replace("(", "").replace(")", "")
            
            approach_data = asteroid["close_approach_data"][0]
            approach_date = approach_data["close_approach_date"]

            exists = (
                db.query(Asteroid)
                .filter(Asteroid.name == clean_name)
                .filter(Asteroid.close_approach_date == approach_date)
                .first()
            )

            if exists:
                continue

            db.add(
                Asteroid(
                    name=clean_name,
                    diameter=asteroid["estimated_diameter"]["meters"]["estimated_diameter_max"],
                    velocity=float(approach_data["relative_velocity"]["kilometers_per_hour"]),
                    miss_distance=float(approach_data["miss_distance"]["kilometers"]),
                    hazardous=asteroid["is_potentially_hazardous_asteroid"],
                    close_approach_date=approach_date
                )
            )
            inserted += 1

    db.commit()

    # Usuwanie starych wpisów (starszych niż 30 dni)
    cutoff = today - timedelta(days=30)
    
    old = (
        db.query(Asteroid)
        .filter(Asteroid.close_approach_date < str(cutoff))
        .all()
    )

    for row in old:
        db.delete(row)

    db.commit()

    print(f"Added {inserted} asteroids")
