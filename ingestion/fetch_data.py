import os
import sys
import requests
from datetime import datetime

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from database import db_manager

NASA_API_KEY = os.getenv("API_NASA")

def fetch_apod():
    if not NASA_API_KEY:
        print("Brak klucza API_NASA")
        return None

    print("\n[1/3] Łączenie z API NASA (APOD)...")
    url = f"https://api.nasa.gov/planetary/apod?api_key={NASA_API_KEY}"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        print(f"POBRANO: Zdjęcie Dnia - '{data.get('title')}'")
        return data
    else:
        print(f"Błąd APOD: {response.status_code}")
        return None

def fetch_iss_position():
    print("\n[2/3] Łączenie z API Open Notify (ISS)...")
    url = "http://api.open-notify.org/iss-now.json"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        lat = data['iss_position']['latitude']
        lon = data['iss_position']['longitude']
        print(f"POBRANO: Pozycja ISS (Szerokość: {lat}, Długość: {lon})")
        return data
    else:
        print(f"Błąd ISS: {response.status_code}")
        return None

def fetch_asteroids():
    if not NASA_API_KEY:
        return None

    today = datetime.now().strftime("%Y-%m-%d")
    print(f"\n[3/3] Łączenie z API NASA NeoWs (Asteroidy z {today})...")
    
    url = f"https://api.nasa.gov/neo/rest/v1/feed?start_date={today}&end_date={today}&api_key={NASA_API_KEY}"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        raw_asteroids = data.get("near_earth_objects", {}).get(today, [])
        
        processed_asteroids = []
        
        for ast in raw_asteroids:
            asteroid_data = {
                "name": ast.get("name"),
                "diameter_min_m": ast["estimated_diameter"]["meters"]["estimated_diameter_min"],
                "diameter_max_m": ast["estimated_diameter"]["meters"]["estimated_diameter_max"],
                "speed_kmh": float(ast["close_approach_data"][0]["relative_velocity"]["kilometers_per_hour"]),
                "miss_distance_km": float(ast["close_approach_data"][0]["miss_distance"]["kilometers"]),
                "is_hazardous": ast.get("is_potentially_hazardous_asteroid")
            }
            processed_asteroids.append(asteroid_data)
            
        print(f"POBRANO: Przetworzono {len(processed_asteroids)} obiektów. Oto one:")
        for a in processed_asteroids:
            print(f"   -> {a['name']} | Max Średnica: {a['diameter_max_m']:.1f} m | Odległość: {a['miss_distance_km']:.0f} km | Prędkość: {a['speed_kmh']:.0f} km/h")
            
        return processed_asteroids
    else:
        print(f"Błąd NeoWs: {response.status_code}")
        return None

if __name__ == "__main__":
    apod_data = fetch_apod()
    iss_data = fetch_iss_position()
    asteroids_data = fetch_asteroids()
    
    print("\n[ZAPIS DO BAZY DANYCH]")
    
    today = datetime.now().strftime("%Y-%m-%d")

    if apod_data:
        db_manager.save_apod(
            fetch_date=today,
            title=apod_data.get('title'),
            url=apod_data.get('url'),
            explanation=apod_data.get('explanation')
        )
        print("Zapisano zdjęcie APOD do bazy.")

    if iss_data:
        lat = float(iss_data['iss_position']['latitude'])
        lon = float(iss_data['iss_position']['longitude'])
        db_manager.save_iss_position(lat, lon)
        print("Zapisano pozycję ISS do bazy.")
        
    if asteroids_data:
        for a in asteroids_data:
            db_manager.save_asteroid(
                fetch_date=today,
                name=a['name'],
                diameter_max_m=a['diameter_max_m'],
                miss_distance_km=a['miss_distance_km'],
                speed_kmh=a['speed_kmh'],
                is_hazardous=a['is_hazardous']
            )
        print("Zapisano dane asteroid do bazy.")

    print("\nEtap akwizycji i zapisu zakończony pomyślnie!")
