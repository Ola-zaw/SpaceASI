from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import sqlite3
import os

app = FastAPI(
    title="Space Dashboard API",
    description="API dostarczające dane o asteroidach i ISS na potrzeby kosmicznego dashboardu."
)

# Konfiguracja CORS (pozwala Frontendowi na komunikację z tym API)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # W wersji produkcyjnej podaje się tu konkretny adres strony
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'space_dashboard.db')

def get_db_connection():
    """Pomocnicza funkcja do łączenia z bazą i zwracania wyników jako słowniki"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

@app.get("/api/iss/latest", tags=["ISS"])
def get_latest_iss_position():
    """Zwraca ostatnią zapisaną pozycję Międzynarodowej Stacji Kosmicznej"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM iss_position ORDER BY timestamp DESC LIMIT 1")
    row = cursor.fetchone()
    conn.close()
    
    if row:
        return dict(row)
    return {"message": "Brak danych o ISS w bazie"}

@app.get("/api/asteroids/latest", tags=["Asteroids"])
def get_latest_asteroids():
    """Zwraca ostatnio pobrane dane o asteroidach"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM asteroids ORDER BY fetch_date DESC LIMIT 10")
    rows = cursor.fetchall()
    conn.close()
    
    return [dict(row) for row in rows]

@app.get("/api/apod/latest", tags=["APOD"])
def get_latest_apod():
    """Zwraca dzisiejsze Astronomiczne Zdjęcie Dnia"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM apod ORDER BY fetch_date DESC LIMIT 1")
    row = cursor.fetchone()
    conn.close()
    
    if row:
        return dict(row)
    return {"message": "Brak danych APOD w bazie"}
