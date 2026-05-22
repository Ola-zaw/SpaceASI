from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from app.database import engine, SessionLocal
from app.models import Base, ISSPosition
from app.models import Asteroid
from app.models import APOD

print(
Base.metadata.tables.keys()
)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)


@app.get("/")
def root():
    return {"message": "Backend działa"}


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


@app.get(
"/asteroids"
)

def get_asteroids():

    db=SessionLocal()


    rows=(

        db.query(
            Asteroid
        )

        .order_by(
            Asteroid.close_approach_date
        )

        .limit(
            10
        )

        .all()

    )


    return[

        {

            "name":
            a.name,

            "diameter":
            round(
                a.diameter
            ),

            "velocity":
            round(
                a.velocity
            ),

            "miss_distance":
            round(
                a.miss_distance
            ),

            "hazardous":
            a.hazardous,

            "date":
            a.close_approach_date

        }

        for a
        in rows

    ]

@app.get(
"/asteroids/stats"
)

def asteroid_stats():

    db = SessionLocal()

    rows = db.query(
        Asteroid
    ).all()


    return {

        "total":
        len(
            rows
        ),

        "hazardous":
        len(
            [
                x
                for x
                in rows
                if x.hazardous
            ]
        ),

        "largest":
        round(

            max(
                x.diameter
                for x
                in rows
            )

        )

    }


@app.get("/apod/latest")
def get_latest_apod():

    db = SessionLocal()

    latest_apod = (

        db.query(APOD)

        .order_by(
            APOD.id.desc()
        )

        .first()

    )


    if latest_apod is None:

        return {

            "title":
            "No APOD yet",

            "image_url":
            "",

            "explanation":
            "NASA data unavailable",

            "date":
            ""

        }


    return {

        "title":
        latest_apod.title,

        "image_url":
        latest_apod.image_url,

        "explanation":
        latest_apod.explanation,

        "date":
        latest_apod.apod_date

    }

@app.get("/iss/history")
def get_iss_history():

    db = SessionLocal()

    history = (
        db.query(ISSPosition)
        .order_by(
            ISSPosition.id.desc()
        )
        .limit(90)
        .all()
    )

    history.reverse()

    return [

        {

            "latitude":
            p.latitude,

            "longitude":
            p.longitude

        }

        for p
        in history

    ]
