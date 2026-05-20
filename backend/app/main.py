from fastapi import FastAPI
from sqlalchemy.orm import Session

from app.database import engine, SessionLocal
from app.models import Base, ISSPosition
from app.models import Asteroid
from app.models import APOD

app = FastAPI()

Base.metadata.create_all(bind=engine)


@app.get("/")
def root():
    return {"message": "Backend działa"}


@app.get("/iss")
def get_iss():

    db: Session = SessionLocal()

    new_position = ISSPosition(
        latitude=50.0,
        longitude=20.0
    )

    db.add(new_position)
    db.commit()

    positions = db.query(ISSPosition).all()

    result = []

    for position in positions:
        result.append({
            "id": position.id,
            "latitude": position.latitude,
            "longitude": position.longitude
        })

    return result


@app.get("/iss/latest")
def get_latest_iss():

    db: Session = SessionLocal()

    latest_position = (
        db.query(ISSPosition)
        .order_by(ISSPosition.id.desc())
        .first()
    )

    return {
        "id": latest_position.id,
        "latitude": latest_position.latitude,
        "longitude": latest_position.longitude,
        "created_at": latest_position.created_at
    }

@app.get("/iss/all")
def get_all_iss():

    db: Session = SessionLocal()

    positions = db.query(ISSPosition).all()

    result = []

    for position in positions:
        result.append({
            "id": position.id,
            "latitude": position.latitude,
            "longitude": position.longitude,
            "created_at": position.created_at
        })

    return result


@app.get("/asteroids")
def get_asteroids():

    db: Session = SessionLocal()

    asteroids = db.query(Asteroid).all()

    result = []

    for asteroid in asteroids:

        result.append({
            "name": asteroid.name,
            "diameter": asteroid.diameter,
            "velocity": asteroid.velocity,
            "miss_distance": asteroid.miss_distance,
            "hazardous": asteroid.hazardous,
            "date": asteroid.close_approach_date
        })

    return result

@app.get("/apod/latest")
def get_latest_apod():

    db: Session = SessionLocal()

    latest_apod = (
        db.query(APOD)
        .order_by(APOD.id.desc())
        .first()
    )

    return {
        "title": latest_apod.title,
        "image_url": latest_apod.image_url,
        "explanation": latest_apod.explanation,
        "date": latest_apod.apod_date
    }