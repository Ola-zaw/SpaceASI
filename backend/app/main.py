from fastapi import FastAPI
from sqlalchemy.orm import Session

from app.database import engine, SessionLocal
from app.models import Base, ISSPosition

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