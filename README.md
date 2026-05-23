# Space Dashboard (Kosmiczny Dashboard)

Space Dashboard to aplikacja webowa prezentująca wybrane dane kosmiczne w czasie rzeczywistym. System integruje informacje o bliskich przelotach asteroid, aktualnej pozycji Międzynarodowej Stacji Kosmicznej (ISS) oraz codziennie dostarcza astronomiczne zdjęcia NASA, prezentując je na interaktywnym dashboardzie.

---

# Wykorzystane źródła danych (Open Data)

Dane pobierane są z następujących źródeł:

## 1. NASA APOD (Astronomy Picture of the Day)

https://api.nasa.gov/

Źródło dostarczające codzienne astronomiczne zdjęcie wraz z opisem naukowym.

Pobierane dane:
- tytuł zdjęcia,
- adres obrazu,
- opis,
- data publikacji.

---

## 2. NASA NeoWs (Near Earth Object Web Service)

https://api.nasa.gov/

Źródło danych o asteroidach bliskich Ziemi.

Pobierane dane:
- nazwa obiektu,
- średnica,
- prędkość,
- odległość od Ziemi,
- status zagrożenia,
- data zbliżenia.

System pobiera dane dla zakresu:

```text
dzisiaj → +7 dni
```

Każde zbliżenie traktowane jest jako osobne zdarzenie.

---

## 3. Open Notify API (ISS Location Now)

http://open-notify.org/Open-Notify-API/ISS-Location-Now/

Źródło aktualnej pozycji Międzynarodowej Stacji Kosmicznej.

Pobierane dane:
- szerokość geograficzna,
- długość geograficzna.

---

# Architektura systemu i technologie

System został zaprojektowany jako aplikacja wielowarstwowa.

## Data Ingestion

Niezależny proces Python odpowiedzialny za pobieranie danych z zewnętrznych API.

Częstotliwość aktualizacji:

| Dane | Częstotliwość |
|---|---|
| ISS | co 5 sekund |
| APOD | przy starcie + co 24 godziny |
| Asteroidy | przy starcie + co 24 godziny |

Proces zapisuje dane do bazy danych i ogranicza liczbę zapytań do zewnętrznych API.

---

# Baza danych

W projekcie wykorzystano:

```text
PostgreSQL 16
```

uruchamiany w kontenerze Docker.

Dane przechowywane są historycznie, ale baza automatycznie usuwa stare rekordy.

Retencja danych:

| Tabela | Zawartość | Retencja |
|---|---|---|
| iss_positions | historia pozycji ISS | ostatnie 5000 punktów |
| apod | zdjęcia dnia NASA | ostatnie 30 rekordów |
| asteroids | dane asteroid | ostatnie 30 dni |

Zasady przechowywania:

- ISS zapisywana jest jako seria punktów czasowych,
- APOD przechowuje historię zdjęć dnia,
- asteroidy przechowują historię zbliżeń,
- rekord asteroid jest unikalny po:

```text
(nazwa + data zbliżenia)
```

---

# Backend

Technologie:

```text
Python
FastAPI
SQLAlchemy
```

Backend udostępnia REST API dla frontendu.

Przykładowe endpointy:

```http
GET /iss/latest
GET /iss/history
GET /apod/latest
GET /asteroids
GET /asteroids/stats
```

Opis endpointów:

| Endpoint | Opis |
|---|---|
| /iss/latest | aktualna pozycja ISS |
| /iss/history | historia pozycji ISS |
| /apod/latest | ostatnie zdjęcie NASA |
| /asteroids | wszystkie zapisane zbliżenia asteroid |
| /asteroids/stats | statystyki unikalnych zbliżeń |

Frontend komunikuje się wyłącznie z backendem.

---

# Frontend

Technologie:

```text
HTML5
JavaScript
Chart.js
Leaflet.js
```

Dashboard prezentuje:

- aktualną pozycję ISS,
- historyczny ślad ruchu ISS,
- zdjęcie dnia NASA,
- tabelę asteroid,
- wykres prędkości asteroid,
- wykres odległości asteroid.

Mapa:
- odświeżanie pozycji ISS co 5 sekund,
- możliwość przybliżania,
- zapamiętywanie ostatniego położenia i zoomu po odświeżeniu strony.

Tabela asteroid:
- prezentuje 10 najbliższych zbliżeń,

Wykresy:
- prędkość asteroid,
- odległość asteroid,
- wyróżnienie niebezpiecznych obiektów.

Statystyki:

- Total - liczba zbliżeń,
- Dangerous - liczba niebezpiecznych zbliżeń,
- zakres dat zapisanych danych (dane z najbliższego tygodnia).

---

# Konteneryzacja

Projekt uruchamiany jest przy użyciu:

```text
Docker
Docker Compose
```

Uruchamiane kontenery:

- PostgreSQL,
- Backend (FastAPI),
- Data Ingestion.

---

# Konfiguracja

Utwórz plik:

```text
.env
```

i uzupełnij:

```env
NASA_API_KEY=...

DATABASE_URL=postgresql://postgres:password@db:5432/space_db

POSTGRES_USER=postgres
POSTGRES_PASSWORD=password
POSTGRES_DB=space_db
```

Plik `.env` nie powinien być commitowany do repozytorium.
