# Space Dashboard (Kosmiczny Dashboard)

**Space Diagram** to aplikacja webowa prezentująca wybrane dane kosmiczne. System integruje informacje o bliskich przelotach asteroid, aktualnej pozycji Międzynarodowej Stacji Kosmicznej (ISS) oraz codziennie dostarcza astronomiczne zdjęcia, prezentując je na interaktywnym dashboardzie.

---

## Wykorzystane źródła danych (Open Data)

Dane pobierane są z następujących źródeł:

1. **[NASA APOD (Astronomy Picture of the Day)](https://api.nasa.gov/)**
   * Zwraca astronomiczne "zdjęcie dnia" wraz z opisem naukowym.

2. **[NASA NeoWs (Near Earth Object Web Service)](https://api.nasa.gov/)**
   * Baza danych o asteroidach bliskich Ziemi.
   * Dostarcza codzienne raporty o przelatujących obiektach (rozmiar, prędkość, odległość od Ziemi, status zagrożenia), które są analizowane i wizualizowane na wykresach.

3. **[Open Notify API (ISS Location Now)](http://open-notify.org/Open-Notify-API/ISS-Location-Now/)**
   * Zwraca aktualne współrzędne geograficzne (długość i szerokość) Międzynarodowej Stacji Kosmicznej.
   * Pozwala na wyrysowanie aktualnej orbity i pozycji stacji na interaktywnej mapie świata.

---

## Architektura systemu i technologie

System został zaprojektowany w architekturze warstwowej i składa się z następujących komponentów:

* **Akwizycja Danych (Data Ingestion):** Skrypt Python pobierający cyklicznie dane z zewnętrznych API.
* **Baza Danych:** `SQLite` - do przechowywania zapytań historycznych i optymalizacji odpytywania API.
* **Backend:** `Python` + `FastAPI` - udostępnia dane na potrzeby frontendu (wystawia REST API).
* **Frontend:** `HTML5` / `JavaScript` z wykorzystaniem bibliotek `Chart.js` (wykresy) oraz `Leaflet.js` (mapa).
* **Środowisko / Konteneryzacja:** `Docker` i `Docker Compose` (środowiska: testowe, deweloperskie, produkcyjne).
