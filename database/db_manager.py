import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'space_dashboard.db')

def get_connection():
    return sqlite3.connect(DB_PATH)

def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS iss_position (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            latitude REAL,
            longitude REAL
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS asteroids (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fetch_date DATE,
            name TEXT,
            diameter_max_m REAL,
            miss_distance_km REAL,
            speed_kmh REAL,
            is_hazardous BOOLEAN
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS apod (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fetch_date DATE,
            title TEXT,
            url TEXT,
            explanation TEXT
        )
    ''')
    
    conn.commit()
    conn.close()
    print("Baza danych i tabele zaktualizowane (dodano APOD).")

def save_iss_position(lat, lon):
    conn = get_connection()
    conn.cursor().execute('INSERT INTO iss_position (latitude, longitude) VALUES (?, ?)', (lat, lon))
    conn.commit()
    conn.close()

def save_asteroid(fetch_date, name, diameter_max_m, miss_distance_km, speed_kmh, is_hazardous):
    conn = get_connection()
    conn.cursor().execute('''
        INSERT INTO asteroids (fetch_date, name, diameter_max_m, miss_distance_km, speed_kmh, is_hazardous) 
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (fetch_date, name, diameter_max_m, miss_distance_km, speed_kmh, is_hazardous))
    conn.commit()
    conn.close()

def save_apod(fetch_date, title, url, explanation):
    conn = get_connection()
    conn.cursor().execute('''
        INSERT INTO apod (fetch_date, title, url, explanation) 
        VALUES (?, ?, ?, ?)
    ''', (fetch_date, title, url, explanation))
    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
