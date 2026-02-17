# URLShortener

A full-stack URL shortener built with:

- **FastAPI** backend for shortening and lookup
- **PostgreSQL** for persistent URL mappings
- **Two Redis instances**:
  - a durable counter store for unique ID generation
  - an LRU cache for fast short-url lookups
- A simple **HTML/CSS/JavaScript** frontend

## Features

- Create short URLs via `POST /shorten`
- Resolve short URLs via `GET /{shorturl}`
- Base62-style encoded short IDs (fixed width)
- Startup table creation through SQLAlchemy metadata
- Redis-backed counter + cache separation

---

## Project Structure

```text
.
├── app/
│   ├── main.py               # FastAPI app, startup lifecycle, exception handlers
│   ├── routers/url.py        # API routes
│   ├── service.py            # Business logic
│   ├── repository.py         # DB/Redis data access
│   ├── database.py           # SQLAlchemy async engine/session
│   └── ...
├── frontend/
│   ├── index.html            # UI
│   ├── script.js             # Calls backend /shorten
│   └── style.css
├── redis/
│   ├── redis-counter.conf    # durable counter Redis
│   └── redis-cache.conf      # LRU cache Redis
├── schema.sql                # Optional schema SQL
└── requirements.txt
```

---

## Prerequisites

Install the following:

- **Git**
- **Python 3.10+**
- **PostgreSQL 13+**
- **Redis 6+**

---

## 1) Clone the repository

```bash
git clone https://github.com/ambi-04/URLShortener.git
cd URLShortener
```

---

## 2) Create and activate a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

On Windows (PowerShell):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

---

## 3) Install dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

> Note: `requirements.txt` currently includes many global/system packages. If installation fails on your machine, create a smaller app-focused requirements file with only the backend dependencies (FastAPI, Uvicorn, SQLAlchemy, asyncpg, redis, python-dotenv, pydantic).

---

## 4) Configure environment variables

Create a `.env` file in the project root:

```env
DATABASE_URL=postgresql+asyncpg://<postgres_user>:<postgres_password>@localhost:5432/<database_name>
API_BASE_URL=http://localhost:8000
```

### What these values are used for

- `DATABASE_URL`: used by SQLAlchemy async engine in `app/database.py`
- `API_BASE_URL`: used when generating the returned short URL in `app/service.py`

---

## 5) Set up PostgreSQL

1. Create a database and user (or reuse an existing one).
2. Ensure `DATABASE_URL` points to it.

You can optionally run the SQL manually:

```bash
psql -U <postgres_user> -d <database_name> -f schema.sql
```

> The app also creates tables on startup using SQLAlchemy metadata.

---

## 6) Start Redis instances

This project expects **two Redis servers**:

- Counter Redis: `localhost:6379`
- Cache Redis: `localhost:6380`

From the repository root, run these in separate terminals:

```bash
redis-server redis/redis-counter.conf
```

```bash
redis-server redis/redis-cache.conf
```

---

## 7) Run the backend API

From the repository root:

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Useful endpoints:

- `GET /` — health/welcome message
- `POST /shorten` — create short URL
- `GET /{shorturl}` — return target URL (with `Location` header)

Swagger docs:

- `http://localhost:8000/docs`

---

## 8) Run the frontend

Option A (simple): open `frontend/index.html` directly in a browser.

Option B (recommended): serve it with a static server:

```bash
cd frontend
python3 -m http.server 5500
```

Then open `http://localhost:5500`.

> Important: `frontend/script.js` currently calls a hardcoded backend URL (`http://192.168.29.77:8000/shorten`).
> Update it to your backend host (for local use: `http://localhost:8000/shorten`).

---

## Quick API Test (without frontend)

```bash
curl -X POST http://localhost:8000/shorten \
  -H "Content-Type: application/json" \
  -d '{"longurl":"https://example.com/very/long/path"}'
```

Example response:

```json
{
  "success": true,
  "message": "shorturl created successfully",
  "shorturl": "http://localhost:8000/00000ab"
}
```

Now resolve it:

```bash
curl -i http://localhost:8000/00000ab
```

---

## Troubleshooting

- **Redis connection errors**: verify both Redis servers are running on ports `6379` and `6380`.
- **Database connection errors**: verify `DATABASE_URL`, Postgres credentials, and database existence.
- **Frontend can’t shorten URLs**: update the hardcoded API URL in `frontend/script.js`.
- **Dependency install issues**: simplify `requirements.txt` for your OS/environment.

---

## License

No license file is currently included in this repository. Add one if you plan to distribute it publicly.
