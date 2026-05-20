# Jak uruchomić projekt Space Dashboard

## 1. Zainstalować Docker Desktop

Pobrać:
https://www.docker.com/products/docker-desktop/

Po instalacji uruchomić Docker Desktop i sprawdzić:

```bash
docker --version
docker compose version
```

---

# 2. Sklonować repo

```bash
git clone <LINK_DO_REPO>
```

Potem:

```bash
cd SpaceASI
```

---

# 3. Utworzyć plik `.env`

W głównym folderze projektu stworzyć plik:

```text
.env
```

i wkleić:

```env
POSTGRES_USER=postgres
POSTGRES_PASSWORD=password
POSTGRES_DB=space_db
```

---

# 4. Uruchomić projekt

W głównym folderze projektu:

```bash
docker compose up --build
```

Docker:

* uruchomi PostgreSQL
* zbuduje backend FastAPI
* uruchomi ingestion service

---

# 5. Sprawdzić backend

Otworzyć w przeglądarce:

```text
http://localhost:8000
```

Powinno działać API.

---

# 6. Swagger

Dokumentacja API:

```text
http://localhost:8000/docs
```

---

# 7. Endpointy ISS

Najnowsza pozycja ISS:

```text
http://localhost:8000/iss/latest
```

Wszystkie pozycje ISS:

```text
http://localhost:8000/iss/all
```

---

# 8. Sprawdzenie PostgreSQL z terminala

Wejście do bazy:

```bash
docker exec -it space_postgres psql -U postgres -d space_db
```

Lista tabel:

```sql
\dt
```

Wyświetlenie danych ISS:

```sql
SELECT * FROM iss_positions;
```

Wyjście:

```sql
\q
```
